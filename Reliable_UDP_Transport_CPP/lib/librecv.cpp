#include <pthread.h>
#include <cstdlib>
#include <map>
#include <cstdint>
#include <cstring>
#include <cstdio>
#include <unistd.h>
#include <errno.h>
#include "lib.h"
#include "utils.h"
#include "protocol.h"
#include <poll.h>
#include <cassert>
#include <sys/timerfd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

using namespace std;

std::map<int, struct connection *> cons;

struct pollfd data_fds[MAX_CONNECTIONS];
/* Used for timers per connection */
struct pollfd timer_fds[MAX_CONNECTIONS];
int fdmax = 0;

static int listen_sock = -1;
static int recv_buffer_size = 9 * 1024;
static int next_conn_id = 0;

pthread_mutex_t table_lock = PTHREAD_MUTEX_INITIALIZER;

static uint32_t checksum(char *data, int len)
{
    uint32_t sum = 2166136261u;

    for (int i = 0; i < len; i++) {
        sum ^= (unsigned char)data[i];
        sum *= 16777619u;
    }

    return sum;
}

static int add_checksum(char *packet, int len)
{
    uint32_t sum = htonl(checksum(packet, len));
    memcpy(packet + len, &sum, sizeof(sum));

    return len + sizeof(sum);
}

static bool valid_checksum(char *packet, int len)
{
    if (len < (int)sizeof(uint32_t))
        return false;

    uint32_t got;
    memcpy(&got, packet + len - sizeof(uint32_t), sizeof(got));
    got = ntohl(got);

    return got == checksum(packet, len - sizeof(uint32_t));
}

static void send_ctrl(int sockfd, sockaddr_in *addr, uint8_t conn_id, uint8_t type,
                      uint16_t ack_num, uint16_t recv_window)
{
    char packet[sizeof(poli_tcp_ctrl_hdr) + sizeof(uint32_t)];
    poli_tcp_ctrl_hdr hdr;

    hdr.protocol_id = POLI_PROTOCOL_ID;
    hdr.conn_id = conn_id;
    hdr.type = type;
    hdr.ack_num = htons(ack_num);
    hdr.recv_window = htons(recv_window);

    memcpy(packet, &hdr, sizeof(hdr));
    int packet_len = add_checksum(packet, sizeof(hdr));

    sendto(sockfd, packet, packet_len, 0, (struct sockaddr *)addr, sizeof(*addr));
}

static bool same_client(sockaddr_in *a, sockaddr_in *b)
{
    return a->sin_addr.s_addr == b->sin_addr.s_addr &&
           a->sin_port == b->sin_port;
}

static void send_synack(connection *con, sockaddr_in *client_addr)
{
    sockaddr_in local_addr;
    socklen_t local_len = sizeof(local_addr);
    memset(&local_addr, 0, sizeof(local_addr));

    getsockname(con->sockfd, (struct sockaddr *)&local_addr, &local_len);

    send_ctrl(listen_sock, client_addr, con->conn_id, TYPE_SYNACK,
              ntohs(local_addr.sin_port), con->recv_buffer_bytes);
}

static bool resend_synack_if_existing(sockaddr_in *client_addr)
{
    bool found = false;

    pthread_mutex_lock(&table_lock);

    for (auto const &it : cons) {
        connection *con = it.second;

        if (same_client(&con->servaddr, client_addr)) {
            send_synack(con, client_addr);
            found = true;
            break;
        }
    }

    pthread_mutex_unlock(&table_lock);

    return found;
}

static void add_connection_socket(connection *con)
{
    assert(fdmax < MAX_CONNECTIONS);

    data_fds[fdmax].fd = con->sockfd;
    data_fds[fdmax].events = POLLIN;
    data_fds[fdmax].revents = 0;

    timer_fds[fdmax].fd = timerfd_create(CLOCK_REALTIME, 0);
    timer_fds[fdmax].events = POLLIN;
    timer_fds[fdmax].revents = 0;

    struct itimerspec spec;
    memset(&spec, 0, sizeof(spec));
    spec.it_value.tv_sec = 1;
    spec.it_value.tv_nsec = 0;
    spec.it_interval.tv_sec = 1;
    spec.it_interval.tv_nsec = 0;
    timerfd_settime(timer_fds[fdmax].fd, 0, &spec, NULL);

    fdmax++;
}

static void move_to_app(connection *con)
{
    while (1) {
        auto it = con->recv_window_buffer.find(con->expected_seq);
        if (it == con->recv_window_buffer.end())
            break;

        for (int i = 0; i < it->second.len; i++)
            con->app_buffer.push_back(it->second.data[i]);

        con->recv_window_buffer.erase(it);
        con->expected_seq++;
    }
}

static void handle_data_packet(connection *con, char *segment, int res)
{
    if (res < (int)(sizeof(poli_tcp_data_hdr) + sizeof(uint32_t)))
        return;

    if (!valid_checksum(segment, res))
        return;

    poli_tcp_data_hdr hdr;
    memcpy(&hdr, segment, sizeof(hdr));

    if (hdr.protocol_id != POLI_PROTOCOL_ID || hdr.conn_id != con->conn_id ||
        hdr.type != TYPE_DATA)
        return;

    uint16_t seq = ntohs(hdr.seq_num);
    uint16_t data_len = ntohs(hdr.len);
    int payload_len = res - (int)sizeof(hdr) - (int)sizeof(uint32_t);

    if (data_len > MAX_DATA_SIZE || data_len != payload_len)
        return;

    if (seq >= con->expected_seq &&
        con->recv_window_buffer.find(seq) == con->recv_window_buffer.end()) {
        stored_segment seg;
        memset(&seg, 0, sizeof(seg));
        seg.seq = seq;
        seg.len = data_len;
        memcpy(seg.data, segment + sizeof(hdr), data_len);

        con->recv_window_buffer[seq] = seg;
        move_to_app(con);
    }

    send_ctrl(con->sockfd, &con->servaddr, con->conn_id, TYPE_ACK,
              seq, con->recv_buffer_bytes);
}

int recv_data(int conn_id, char *buffer, int len)
{
    int size = 0;
    connection *con = NULL;

    pthread_mutex_lock(&table_lock);

    if (cons.find(conn_id) != cons.end())
        con = cons[conn_id];

    pthread_mutex_unlock(&table_lock);

    if (con == NULL)
        return -1;

    while (size == 0) {
        pthread_mutex_lock(&con->con_lock);

        /* We will write code here as to not have sync problems with recv_handler */

        while (size < len && !con->app_buffer.empty()) {
            buffer[size++] = con->app_buffer.front();
            con->app_buffer.pop_front();
        }

        pthread_mutex_unlock(&con->con_lock);

        if (size == 0)
            usleep(1000);
    }

    return size;
}

void *receiver_handler(void *arg)
{

    char segment[MAX_SEGMENT_SIZE];
    DEBUG_PRINT("Starting recviver handler\n");

    while (1) {
        pollfd local_fds[MAX_CONNECTIONS];
        connection *local_cons[MAX_CONNECTIONS];
        int local_size = 0;

        /* Facem o lista locala de socket-uri pentru conexiunile active */
        pthread_mutex_lock(&table_lock);

        for (auto const &it : cons) {
            if (local_size >= MAX_CONNECTIONS)
                break;

            local_fds[local_size].fd = it.second->sockfd;
            local_fds[local_size].events = POLLIN;
            local_fds[local_size].revents = 0;
            local_cons[local_size] = it.second;
            local_size++;
        }

        pthread_mutex_unlock(&table_lock);

        if (local_size == 0) {
            usleep(1000);
            continue;
        }

        int ready = poll(local_fds, local_size, 1);
        if (ready <= 0)
            continue;

        for (int i = 0; i < local_size; i++) {
            if (!(local_fds[i].revents & POLLIN))
                continue;

            connection *con = local_cons[i];

            sockaddr_in from_addr;
            socklen_t from_len = sizeof(from_addr);

            int res = recvfrom(local_fds[i].fd, segment, sizeof(segment), MSG_DONTWAIT,
                               (struct sockaddr *)&from_addr, &from_len);

            if (res <= 0)
                continue;

            pthread_mutex_lock(&con->con_lock);

            /* Handle segment received from the sender. We use this between locks
            as to not have synchronization issues with the recv_data calls which are
            on the main thread */

            handle_data_packet(con, segment, res);

            pthread_mutex_unlock(&con->con_lock);
        }
    }


}

int wait4connect(uint32_t ip, uint16_t port)
{
    /* TODO: Implement the Three Way Handshake on the receiver part. This blocks
     * until a connection is established. */

    if (listen_sock < 0) {
        listen_sock = socket(AF_INET, SOCK_DGRAM, 0);
        assert(listen_sock >= 0);

        int yes = 1;
        setsockopt(listen_sock, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes));

        int sock_buf_size = 1 << 20;
        setsockopt(listen_sock, SOL_SOCKET, SO_RCVBUF, &sock_buf_size, sizeof(sock_buf_size));

        sockaddr_in listen_addr;
        memset(&listen_addr, 0, sizeof(listen_addr));
        listen_addr.sin_family = AF_INET;
        listen_addr.sin_addr.s_addr = ip;
        listen_addr.sin_port = port;
        int rc = bind(listen_sock, (struct sockaddr *)&listen_addr, sizeof(listen_addr));
        assert(rc >= 0);
    }

    char msg_buf[sizeof(poli_tcp_ctrl_hdr) + sizeof(uint32_t)];
    sockaddr_in client_addr;
    socklen_t client_len;

    while (1) {
        client_len = sizeof(client_addr);

        int n = recvfrom(listen_sock, msg_buf, sizeof(msg_buf), 0,
                         (struct sockaddr *)&client_addr, &client_len);

        if (n < (int)(sizeof(poli_tcp_ctrl_hdr) + sizeof(uint32_t)))
            continue;

        if (!valid_checksum(msg_buf, n))
            continue;

        poli_tcp_ctrl_hdr msg;
        memcpy(&msg, msg_buf, sizeof(msg));

        if (msg.protocol_id != POLI_PROTOCOL_ID || msg.type != TYPE_SYN)
            continue;

        if (resend_synack_if_existing(&client_addr))
            continue;

        struct connection *con = new connection();
        int conn_id = next_conn_id++;

        /* This can be used to set a timer on a socket, useful once we received a
         * SYN. You may want to disable by setting the time to 0 (tv_sec = 0,
         * tv_usec = 0)
        struct timeval tv;
        tv.tv_sec = 2;
        tv.tv_usec = 100000;
        if (setsockopt(con->sockfd, SOL_SOCKET, SO_RCVTIMEO,&tv,sizeof(tv)) < 0) {
            perror("Error");
        } */

        /* Receive SYN on the connection socket. Create a new socket and bind it to
         * the chosen port. Send the data port number via SYN-ACK to the client */
        con->sockfd = socket(AF_INET, SOCK_DGRAM, 0);
        assert(con->sockfd >= 0);

        int data_buf_size = 1 << 20;
        setsockopt(con->sockfd, SOL_SOCKET, SO_RCVBUF, &data_buf_size, sizeof(data_buf_size));

        sockaddr_in data_addr;
        memset(&data_addr, 0, sizeof(data_addr));
        data_addr.sin_family = AF_INET;
        data_addr.sin_addr.s_addr = ip;
        data_addr.sin_port = htons(10000 + conn_id);

        while (bind(con->sockfd, (struct sockaddr *)&data_addr, sizeof(data_addr)) < 0)
            data_addr.sin_port = htons(ntohs(data_addr.sin_port) + 1);

        con->conn_id = conn_id;
        con->servaddr = client_addr;
        con->expected_seq = 0;
        con->recv_buffer_bytes = recv_buffer_size;
        con->max_window_seq = recv_buffer_size / MAX_DATA_SIZE;
        if (con->max_window_seq < 1)
            con->max_window_seq = 1;

        pthread_mutex_init(&con->con_lock, NULL);

        pthread_mutex_lock(&table_lock);

        cons.insert({conn_id, con});

        /* Since we can have multiple connection, we want to know if data is available
           on the socket used by a given connection. We use POLL for this */
        add_connection_socket(con);

        pthread_mutex_unlock(&table_lock);

        for (int i = 0; i < 20; i++) {
            send_ctrl(listen_sock, &client_addr, conn_id, TYPE_SYNACK,
                      ntohs(data_addr.sin_port), recv_buffer_size);
            usleep(500);
        }

        DEBUG_PRINT("Connection established!");

        return conn_id;
    }
}

void init_receiver(int recv_buffer_bytes)
{
    pthread_t thread1;
    int ret;

    /* TODO: Create the connection socket and bind it to 8031 */

    recv_buffer_size = recv_buffer_bytes;

    ret = pthread_create( &thread1, NULL, receiver_handler, NULL);
    assert(ret == 0);
}

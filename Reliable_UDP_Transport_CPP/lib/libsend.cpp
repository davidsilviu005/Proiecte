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
#include <cassert>
#include <poll.h>
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

pthread_mutex_t table_lock = PTHREAD_MUTEX_INITIALIZER;

static int speed_mbps = 8;
static int delay_ms = 2;
static int next_conn_id = 0;

static double time_diff_ms(struct timespec start, struct timespec end)
{
    return (end.tv_sec - start.tv_sec) * 1000.0 +
           (end.tv_nsec - start.tv_nsec) / 1000000.0;
}

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

    uint32_t received_sum;
    memcpy(&received_sum, packet + len - sizeof(uint32_t), sizeof(received_sum));
    received_sum = ntohl(received_sum);

    return received_sum == checksum(packet, len - sizeof(uint32_t));
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

static void send_segment(connection *con, stored_segment *seg)
{
    char packet[MAX_SEGMENT_SIZE];
    poli_tcp_data_hdr hdr;

    hdr.protocol_id = POLI_PROTOCOL_ID;
    hdr.conn_id = con->conn_id;
    hdr.type = TYPE_DATA;
    hdr.seq_num = htons(seg->seq);
    hdr.len = htons(seg->len);

    memcpy(packet, &hdr, sizeof(hdr));
    memcpy(packet + sizeof(hdr), seg->data, seg->len);

    int packet_len = add_checksum(packet, sizeof(hdr) + seg->len);

    sendto(con->sockfd, packet, packet_len, 0,
           (struct sockaddr *)&con->servaddr, sizeof(con->servaddr));
}

static int window_limit(connection *con)
{
    int limit = (int)con->cwnd;

    if (limit < 1)
        limit = 1;

    if (limit > con->max_window_seq)
        limit = con->max_window_seq;

    if (con->recv_window > 0) {
        int recv_limit = con->recv_window / MAX_DATA_SIZE;

        if (recv_limit < 1)
            recv_limit = 1;

        if (limit > recv_limit)
            limit = recv_limit;
    }

    return limit;
}

static void handle_ack(connection *con, char *buf, int len)
{
    if (len < (int)(sizeof(poli_tcp_ctrl_hdr) + sizeof(uint32_t)))
        return;

    if (!valid_checksum(buf, len))
        return;

    poli_tcp_ctrl_hdr hdr;
    memcpy(&hdr, buf, sizeof(hdr));

    if (hdr.protocol_id != POLI_PROTOCOL_ID || hdr.conn_id != con->conn_id)
        return;

    if (hdr.type == TYPE_SYNACK) {
        send_ctrl(con->sockfd, &con->servaddr, con->conn_id, TYPE_ACK, 0, 0);
        return;
    }

    if (hdr.type != TYPE_ACK)
        return;

    uint16_t ack = ntohs(hdr.ack_num);
    con->recv_window = ntohs(hdr.recv_window);

    if (con->send_window.erase(ack)) {
        if (con->cwnd < con->ssthresh)
            con->cwnd += 1.0;
        else
            con->cwnd += 1.0 / con->cwnd;

        if (con->cwnd > con->max_window_seq)
            con->cwnd = con->max_window_seq;
    }
}

int send_data(int conn_id, char *buffer, int len)
{
    int size = 0;

    pthread_mutex_lock(&table_lock);
    bool exists = (cons.find(conn_id) != cons.end());
    connection *con = exists ? cons[conn_id] : NULL;
    pthread_mutex_unlock(&table_lock);

    if (!exists)
        return -1;

    pthread_mutex_lock(&con->con_lock);

    /* We will write code here as to not have sync problems with sender_handler */

    if ((int)con->send_window.size() >= window_limit(con)) {
        pthread_mutex_unlock(&con->con_lock);
        usleep(1000);
        return -1;
    }

    size = len;
    if (size > MAX_DATA_SIZE)
        size = MAX_DATA_SIZE;

    stored_segment seg;
    memset(&seg, 0, sizeof(seg));
    seg.seq = con->next_seq++;
    seg.len = size;
    memcpy(seg.data, buffer, size);

    /* Tin minte momentul trimiterii pentru fiecare segment */
    clock_gettime(CLOCK_MONOTONIC, &seg.send_time);

    con->send_window[seg.seq] = seg;
    send_segment(con, &con->send_window[seg.seq]);

    pthread_mutex_unlock(&con->con_lock);

    return size;
}

void *sender_handler(void *arg)
{
    int res = 0;
    char buf[MAX_SEGMENT_SIZE];

    while (1) {
        pthread_mutex_lock(&table_lock);
        int has_connections = !cons.empty();
        pthread_mutex_unlock(&table_lock);

        if (!has_connections) {
            usleep(1000);
            continue;
        }

        int conn_id = -1;
        do {
            res = recv_message_or_timeout(buf, MAX_SEGMENT_SIZE, &conn_id);
            if (res == -14)
                usleep(1000);
        } while (res == -14);

        pthread_mutex_lock(&table_lock);
        bool exists = (cons.find(conn_id) != cons.end());
        connection *con = exists ? cons[conn_id] : NULL;
        pthread_mutex_unlock(&table_lock);

        if (!exists)
            continue;

        pthread_mutex_lock(&con->con_lock);

        /* Handle segment received from the receiver. We use this between locks
        as to not have synchronization issues with the send_data calls which are
        on the main thread */

        if (res == -1) {
            struct timespec now;
            int retransmitted = 0;

            clock_gettime(CLOCK_MONOTONIC, &now);

            for (auto &it : con->send_window) {
                if (time_diff_ms(it.second.send_time, now) >= TIMEOUT_SEND(delay_ms)) {
                    send_segment(con, &it.second);
                    it.second.send_time = now;
                    retransmitted = 1;
                }
            }

            /* Daca a expirat ceva, reducem fereastra si continuam mai prudent */
            if (retransmitted) {
                con->ssthresh = (int)(con->cwnd / 2.0);
                if (con->ssthresh < 2)
                    con->ssthresh = 2;

                con->cwnd = con->ssthresh;
            }
        } else {
            handle_ack(con, buf, res);
        }

        pthread_mutex_unlock(&con->con_lock);
    }
}

int setup_connection(uint32_t ip, uint16_t port)
{
    /* Implement the sender part of the Three Way Handshake. Blocks
    until the connection is established */

    struct connection *con = new connection();
    int conn_id = next_conn_id++;

    con->sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    assert(con->sockfd >= 0);

    memset(&con->servaddr, 0, sizeof(con->servaddr));
    con->servaddr.sin_family = AF_INET;
    con->servaddr.sin_addr.s_addr = ip;
    con->servaddr.sin_port = port;

    /* // This can be used to set a timer on a socket
    struct timeval tv;
    tv.tv_sec = 2;
    tv.tv_usec = 100000;
    if (setsockopt(con->sockfd, SOL_SOCKET, SO_RCVTIMEO,&tv,sizeof(tv)) < 0) {
        perror("Error");
    } */

    struct timeval tv;
    tv.tv_sec = 0;
    tv.tv_usec = 100000;
    setsockopt(con->sockfd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

    /* We will send the SYN on 8031. Then we will receive a SYN-ACK with the connection
     * port. We can use con->sockfd for both cases, but we will need to update server_addr
     * with the port received via SYN-ACK */

    char packet[sizeof(poli_tcp_ctrl_hdr) + sizeof(uint32_t)];
    char reply_buf[sizeof(poli_tcp_ctrl_hdr) + sizeof(uint32_t)];

    poli_tcp_ctrl_hdr syn;
    memset(&syn, 0, sizeof(syn));
    syn.protocol_id = POLI_PROTOCOL_ID;
    syn.conn_id = conn_id;
    syn.type = TYPE_SYN;

    memcpy(packet, &syn, sizeof(syn));
    int packet_len = add_checksum(packet, sizeof(syn));

    while (1) {
        sendto(con->sockfd, packet, packet_len, 0,
               (struct sockaddr *)&con->servaddr, sizeof(con->servaddr));

        int res = recvfrom(con->sockfd, reply_buf, sizeof(reply_buf), 0, NULL, NULL);

        if (res < (int)(sizeof(poli_tcp_ctrl_hdr) + sizeof(uint32_t)))
            continue;

        if (!valid_checksum(reply_buf, res))
            continue;

        poli_tcp_ctrl_hdr synack;
        memcpy(&synack, reply_buf, sizeof(synack));

        if (synack.protocol_id == POLI_PROTOCOL_ID && synack.type == TYPE_SYNACK) {
            con->conn_id = synack.conn_id;
            con->servaddr.sin_port = synack.ack_num;
            con->recv_window = ntohs(synack.recv_window);
            break;
        }
    }

    for (int i = 0; i < 10; i++)
        send_ctrl(con->sockfd, &con->servaddr, con->conn_id, TYPE_ACK, 0, 0);

    tv.tv_sec = 0;
    tv.tv_usec = 0;
    setsockopt(con->sockfd, SOL_SOCKET, SO_RCVTIMEO, &tv, sizeof(tv));

    int bdp_bytes = speed_mbps * 1000000 / 8 * (2 * delay_ms + 30) / 1000;

    con->max_window_seq = bdp_bytes / MAX_DATA_SIZE;
    if (con->max_window_seq < 8)
        con->max_window_seq = 8;
    if (con->max_window_seq > 64)
        con->max_window_seq = 64;

    con->next_seq = 0;
    con->ssthresh = con->max_window_seq;
    con->cwnd = 1.0;

    if (con->recv_window <= 0)
        con->recv_window = 9 * 1024;

    /* Since we can have multiple connection, we want to know if data is available
       on the socket used by a given connection. We use POLL for this */
    pthread_mutex_lock(&table_lock);

    data_fds[fdmax].fd = con->sockfd;
    data_fds[fdmax].events = POLLIN;
    data_fds[fdmax].revents = 0;

    /* Timerul verifica periodic daca exista segmente vechi netrimise corect */
    timer_fds[fdmax].fd = timerfd_create(CLOCK_REALTIME, 0);
    timer_fds[fdmax].events = POLLIN;
    timer_fds[fdmax].revents = 0;

    struct itimerspec spec;
    memset(&spec, 0, sizeof(spec));
    spec.it_value.tv_sec = 0;
    spec.it_value.tv_nsec = 10 * 1000000;
    spec.it_interval.tv_sec = 0;
    spec.it_interval.tv_nsec = 10 * 1000000;
    timerfd_settime(timer_fds[fdmax].fd, 0, &spec, NULL);

    fdmax++;

    pthread_mutex_init(&con->con_lock, NULL);
    cons.insert({conn_id, con});

    pthread_mutex_unlock(&table_lock);

    DEBUG_PRINT("Connection established!");

    return conn_id;
}

void init_sender(int speed, int delay)
{
    pthread_t thread1;
    int ret;

    speed_mbps = speed;
    delay_ms = delay;

    /* Create a thread that will*/
    ret = pthread_create(&thread1, NULL, sender_handler, NULL);
    assert(ret == 0);
}

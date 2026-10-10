#include <sys/socket.h>
#include <sys/types.h>
#include <sys/timerfd.h>
#include <netinet/ip.h>
#include <stdio.h>
#include <cstdint>
#include "lib.h"
#include <vector>
#include <map>
#include <cstring>
#include <assert.h>
#include <unistd.h>
#include <cstdlib>
#include <pthread.h>
#include <sys/poll.h>
#include <fcntl.h>

using namespace std;

/* We use extern to use the variables defined either in
   librecv or libsend */
extern std::map<int, struct connection *> cons;
extern struct pollfd data_fds[MAX_CONNECTIONS];
extern struct pollfd timer_fds[MAX_CONNECTIONS];
extern int fdmax;

extern pthread_mutex_t table_lock;

int recv_message_or_timeout(char *buff, size_t len, int *conn_id)
{
    struct pollfd local_data_fds[MAX_CONNECTIONS];
    struct pollfd local_timer_fds[MAX_CONNECTIONS];
    int local_fdmax = 0;

    /* Copiez local tabelele, ca poll-ul sa lucreze pe o stare stabila */
    pthread_mutex_lock(&table_lock);

    local_fdmax = fdmax;
    for (int i = 0; i < local_fdmax; i++) {
        local_data_fds[i] = data_fds[i];
        local_timer_fds[i] = timer_fds[i];
    }

    pthread_mutex_unlock(&table_lock);

    if (local_fdmax == 0)
        return -14;

    int ret_data = poll(local_data_fds, local_fdmax, 0);
    int ret_timer = poll(local_timer_fds, local_fdmax, 0);

    if (ret_data < 0 || ret_timer < 0)
        return -14;

    for (int i = 0; i < local_fdmax; i++) {
        if (local_data_fds[i].revents & POLLIN) {
            struct sockaddr_in servaddr;
            socklen_t slen = sizeof(struct sockaddr_in);

            int n = recvfrom(local_data_fds[i].fd, buff, len, MSG_DONTWAIT,
                             (struct sockaddr *)&servaddr, &slen);

            if (n < 0)
                continue;

            pthread_mutex_lock(&table_lock);

            int found_conn = -1;
            for (auto const &it : cons) {
                if (it.second->sockfd == local_data_fds[i].fd) {
                    found_conn = it.first;
                    break;
                }
            }

            pthread_mutex_unlock(&table_lock);

            if (found_conn != -1) {
                *conn_id = found_conn;
                return n;
            }
        }

        if (local_timer_fds[i].revents & POLLIN) {
            char dummybuf[8];
            int n = read(local_timer_fds[i].fd, dummybuf, 8);

            if (n < 0)
                continue;

            pthread_mutex_lock(&table_lock);

            int found_conn = -1;
            for (auto const &it : cons) {
                if (it.second->sockfd == local_data_fds[i].fd) {
                    found_conn = it.first;
                    break;
                }
            }

            pthread_mutex_unlock(&table_lock);

            if (found_conn != -1) {
                *conn_id = found_conn;
                return -1;
            }
        }
    }

    return -14;
}

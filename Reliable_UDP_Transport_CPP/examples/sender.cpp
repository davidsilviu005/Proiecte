#include "lib.h"

#include <arpa/inet.h>
#include <cerrno>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>

int main(int argc, char **argv)
{
    if (argc != 4) {
        std::fprintf(stderr, "Usage: %s <IPv4 address> <port> <message>\n", argv[0]);
        return 1;
    }

    char *end = nullptr;
    long port = std::strtol(argv[2], &end, 10);
    if (*end != '\0' || port < 1 || port > 65535) {
        std::fprintf(stderr, "Invalid port\n");
        return 1;
    }

    in_addr ip{};
    if (inet_pton(AF_INET, argv[1], &ip) != 1) {
        std::fprintf(stderr, "Invalid IPv4 address\n");
        return 1;
    }

    init_sender(8, 2);
    int connection = setup_connection(ip.s_addr, htons(static_cast<uint16_t>(port)));

    char *message = argv[3];
    int length = static_cast<int>(std::strlen(message));
    int sent = 0;
    while (sent < length) {
        int count = send_data(connection, message + sent, length - sent);
        if (count > 0) {
            sent += count;
        } else {
            usleep(1000);
        }
    }

    // Keep the process alive briefly so the background handler can receive ACKs.
    usleep(500000);
    return 0;
}

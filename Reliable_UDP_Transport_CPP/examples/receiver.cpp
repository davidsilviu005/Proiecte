#include "lib.h"

#include <arpa/inet.h>
#include <cstdio>
#include <cstdlib>

int main(int argc, char **argv)
{
    if (argc != 2) {
        std::fprintf(stderr, "Usage: %s <port>\n", argv[0]);
        return 1;
    }

    char *end = nullptr;
    long port = std::strtol(argv[1], &end, 10);
    if (*end != '\0' || port < 1 || port > 65535) {
        std::fprintf(stderr, "Invalid port\n");
        return 1;
    }

    init_receiver(64 * 1024);
    int connection = wait4connect(INADDR_ANY, htons(static_cast<uint16_t>(port)));

    char buffer[1024];
    int received = recv_data(connection, buffer, sizeof(buffer));
    if (received <= 0) {
        std::fprintf(stderr, "Receive failed\n");
        return 1;
    }

    std::fwrite(buffer, 1, received, stdout);
    std::fputc('\n', stdout);
    return 0;
}

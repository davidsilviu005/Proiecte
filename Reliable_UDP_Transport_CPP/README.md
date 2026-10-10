# Reliable UDP Transport Layer

A C++ networking project that adds delivery and ordering mechanisms on top of UDP. It provides sender and receiver APIs plus a small loopback demo. The protocol is an educational implementation, not a replacement for TCP.

## What it implements

- SYN, SYN-ACK, and ACK connection setup
- Sequence numbers, acknowledgments, and checksums
- A sender window with timeout-based retransmission
- Out-of-order buffering and ordered delivery at the receiver
- Simplified slow start and congestion avoidance
- Per-connection state with mutex-protected access

## Build

Requires Linux, `g++` with C++17 support, `make`, and POSIX threads:

```bash
make          # builds sender and receiver static libraries
make demo     # builds the loopback examples as well
```

The sender API is in `libreliable_udp_sender.a`; the receiver API is in `libreliable_udp_receiver.a`. Include `lib/include/lib.h` and link with `-pthread`. Run `make clean` to remove build products.

## Loopback demo

In two Linux terminals, run the receiver first:

```bash
./examples/udp_receiver 8031
./examples/udp_sender 127.0.0.1 8031 "Hello over UDP"
```

The receiver prints the message. The demo transfers one short text message; the library API supports sending a stream of bytes in segments, but an application must define its own message framing and lifecycle.

## Project layout and scope

- `lib/libsend.cpp`: sender window, ACK processing, retransmission, and connection setup
- `lib/librecv.cpp`: receiver buffer, ordered delivery, and connection setup
- `lib/libcommon.cpp`: shared polling and timer helper
- `lib/include/`: protocol headers and public API
- `examples/`: small sender and receiver programs added to demonstrate the library
- `docs/original-notes-ro.txt`: original implementation notes in Romanian

The original archive contained the library code but did not include the `client.cpp` and `server.cpp` files named in its Makefile. The Makefile here builds the available library sources, and the added `examples/` programs provide a way to run a basic demo. No license is supplied with the original archive.

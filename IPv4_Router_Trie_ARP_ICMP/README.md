# IPv4 Router with Trie-Based Routing

A Linux packet-forwarding project written in C. The router reads a route table, uses a binary trie for longest-prefix matching, resolves next-hop MAC addresses with ARP, and returns ICMP messages when a packet cannot be forwarded.

## What it implements

- **Longest-prefix matching:** routes are inserted into a bitwise trie; IPv4 lookups take at most 32 steps.
- **ARP:** replies to requests for the router's addresses, learns IP-to-MAC mappings, and queues packets while a next-hop address is being resolved.
- **IPv4 forwarding:** checks the IP header checksum, decrements TTL, recomputes the checksum, and sends the frame on the selected interface.
- **ICMP:** answers echo requests and generates Time Exceeded or Destination Unreachable responses when appropriate.

## Build

Requires Linux, `gcc`, and `make`:

```bash
make
```

The build produces `router`. Run `make clean` to remove generated files. The code compiles on Ubuntu with GCC.

## Running it

The included helper library uses Linux raw packet sockets and expects **three network interfaces**. It also refers to the interface names `rr-0-1`, `r-0`, and `r-1` when querying their IP and MAC addresses. A matching virtual network or equivalent setup is required, along with permission to open raw sockets. The route-table files and the original network topology are not included in this project.

With the expected interfaces and a route table available, the invocation is:

```bash
sudo ./router path/to/routes.txt rr-0-1 r-0 r-1
```

Each route-table row contains a destination prefix, next hop, subnet mask, and output interface index. The route-table parser is provided in `lib/lib.c`.

## Evidence and source layout

The [`docs/arp-cache-and-ping.png`](docs/arp-cache-and-ping.png) screenshot shows ARP resolution on the first ping and a cached mapping on the second. The [`docs/icmp-errors.png`](docs/icmp-errors.png) screenshot shows TTL expiration and an unreachable destination. These are captures from the original lab environment; they are not a substitute for the missing topology files.

- `router.c`: forwarding logic, trie, ARP handling, packet queueing, and ICMP
- `include/`: packet structures and helper interfaces
- `lib/`: Linux link-layer helper and queue implementation
- `docs/`: original notes and packet captures

This project includes coursework-provided helper code alongside the router implementation. No license is supplied with the original archive.

#include "protocols.h"
#include "lib.h"
#include "queue.h"

#include <arpa/inet.h>
#include <string.h>
#include <stdlib.h>

struct packet_q {
	char *buf;
	size_t len;
	int interface;
	uint32_t next_hop;
};

struct trie_node {
	struct trie_node *left;
	struct trie_node *right;
	struct route_table_entry *route;
};

struct route_table_entry *rtable;
int rtable_len;

struct arp_table_entry *arp_table;
int arp_table_len;

uint32_t *arp_pending;
int arp_pending_len;

queue q;
struct trie_node *trie_root;

int mask_len(uint32_t mask)
{
	int cnt = 0;
	mask = ntohl(mask);

	while (mask) {
		if (mask & 1) {
			cnt++;
		}
		mask >>= 1;
	}

	return cnt;
}

struct trie_node *new_node()
{
	struct trie_node *node = malloc(sizeof(struct trie_node));
	DIE(node == NULL, "malloc failed");

	node->left = NULL;
	node->right = NULL;
	node->route = NULL;

	return node;
}

void insert_route(struct route_table_entry *r)
{
	uint32_t prefix = ntohl(r->prefix);
	int len = mask_len(r->mask);

	struct trie_node *node = trie_root;

	for (int i = 31; i >= 32 - len; i--) {
		int bit = (prefix >> i) & 1;

		if (bit == 0) {
			if (node->left == NULL) {
				node->left = new_node();
			}
			node = node->left;
		} else {
			if (node->right == NULL) {
				node->right = new_node();
			}
			node = node->right;
		}
	}

	node->route = r;
}

void build_trie()
{
	trie_root = new_node();

	for (int i = 0; i < rtable_len; i++) {
		insert_route(&rtable[i]);
	}
}

struct route_table_entry *best_route(uint32_t dest_ip)
{
	uint32_t ip = ntohl(dest_ip);
	struct trie_node *node = trie_root;
	struct route_table_entry *best = NULL;

	for (int i = 31; i >= 0; i--) {
		if (node == NULL) {
			break;
		}

		if (node->route != NULL) {
			best = node->route;
		}

		int bit = (ip >> i) & 1;

		if (bit == 0) {
			node = node->left;
		} else {
			node = node->right;
		}
	}

	if (node != NULL && node->route != NULL) {
		best = node->route;
	}

	return best;
}

struct arp_table_entry *arp_entry(uint32_t ip)
{
	for (int i = 0; i < arp_table_len; i++) {
		if (arp_table[i].ip == ip) {
			return &arp_table[i];
		}
	}

	return NULL;
}

void add_arp(uint32_t ip, uint8_t *mac)
{
	for (int i = 0; i < arp_table_len; i++) {
		if (arp_table[i].ip == ip) {
			memcpy(arp_table[i].mac, mac, 6);
			return;
		}
	}

	arp_table[arp_table_len].ip = ip;
	memcpy(arp_table[arp_table_len].mac, mac, 6);
	arp_table_len++;
}

int router_ip(uint32_t ip)
{
	for (int i = 0; i < ROUTER_NUM_INTERFACES; i++) {
		if (ip == inet_addr(get_interface_ip(i))) {
			return 1;
		}
	}

	return 0;
}

int good_checksum(struct ip_hdr *ip_hdr)
{
	uint16_t old = ip_hdr->checksum;
	ip_hdr->checksum = 0;

	uint16_t now = htons(checksum((uint16_t *)ip_hdr, ip_hdr->ihl * 4));
	ip_hdr->checksum = old;

	return old == now;
}

int pending(uint32_t ip)
{
	for (int i = 0; i < arp_pending_len; i++) {
		if (arp_pending[i] == ip) {
			return 1;
		}
	}

	return 0;
}

void add_pending(uint32_t ip)
{
	if (pending(ip)) {
		return;
	}

	arp_pending[arp_pending_len++] = ip;
}

void del_pending(uint32_t ip)
{
	for (int i = 0; i < arp_pending_len; i++) {
		if (arp_pending[i] == ip) {
			for (int j = i; j < arp_pending_len - 1; j++) {
				arp_pending[j] = arp_pending[j + 1];
			}
			arp_pending_len--;
			return;
		}
	}
}

void send_with_mac(char *buf, size_t len, int interface, uint8_t *mac)
{
	struct ether_hdr *eth_hdr = (struct ether_hdr *)buf;

	memcpy(eth_hdr->ethr_dhost, mac, 6);
	get_interface_mac(interface, eth_hdr->ethr_shost);

	send_to_link(len, buf, interface);
}

void put_packet(char *buf, size_t len, int interface, uint32_t next_hop)
{
	struct packet_q *p = malloc(sizeof(struct packet_q));
	DIE(p == NULL, "malloc failed");

	p->buf = malloc(len);
	DIE(p->buf == NULL, "malloc failed");

	memcpy(p->buf, buf, len);
	p->len = len;
	p->interface = interface;
	p->next_hop = next_hop;

	queue_enq(q, p);
}

void solve_queue(uint32_t ip)
{
	queue aux = create_queue();

	while (!queue_empty(q)) {
		struct packet_q *p = queue_deq(q);
		struct arp_table_entry *a = arp_entry(p->next_hop);

		if (p->next_hop == ip && a != NULL) {
			send_with_mac(p->buf, p->len, p->interface, a->mac);
			free(p->buf);
			free(p);
		} else {
			queue_enq(aux, p);
		}
	}

	while (!queue_empty(aux)) {
		queue_enq(q, queue_deq(aux));
	}
}

void send_arp_req(uint32_t ip, int interface)
{
	char buf[MAX_PACKET_LEN];
	memset(buf, 0, MAX_PACKET_LEN);

	struct ether_hdr *eth_hdr = (struct ether_hdr *)buf;
	struct arp_hdr *arp_hdr = (struct arp_hdr *)(buf + sizeof(struct ether_hdr));

	memset(eth_hdr->ethr_dhost, 0xff, 6);
	get_interface_mac(interface, eth_hdr->ethr_shost);
	eth_hdr->ethr_type = htons(0x0806);

	arp_hdr->hw_type = htons(1);
	arp_hdr->proto_type = htons(0x0800);
	arp_hdr->hw_len = 6;
	arp_hdr->proto_len = 4;
	arp_hdr->opcode = htons(1);

	get_interface_mac(interface, arp_hdr->shwa);
	arp_hdr->sprotoa = inet_addr(get_interface_ip(interface));

	memset(arp_hdr->thwa, 0, 6);
	arp_hdr->tprotoa = ip;

	send_to_link(sizeof(struct ether_hdr) + sizeof(struct arp_hdr), buf, interface);
}

void send_arp_rep(char *buf, int interface)
{
	char reply[MAX_PACKET_LEN];
	memset(reply, 0, MAX_PACKET_LEN);

	struct ether_hdr *old_eth = (struct ether_hdr *)buf;
	struct arp_hdr *old_arp = (struct arp_hdr *)(buf + sizeof(struct ether_hdr));

	struct ether_hdr *eth_hdr = (struct ether_hdr *)reply;
	struct arp_hdr *arp_hdr = (struct arp_hdr *)(reply + sizeof(struct ether_hdr));

	memcpy(eth_hdr->ethr_dhost, old_eth->ethr_shost, 6);
	get_interface_mac(interface, eth_hdr->ethr_shost);
	eth_hdr->ethr_type = htons(0x0806);

	arp_hdr->hw_type = htons(1);
	arp_hdr->proto_type = htons(0x0800);
	arp_hdr->hw_len = 6;
	arp_hdr->proto_len = 4;
	arp_hdr->opcode = htons(2);

	get_interface_mac(interface, arp_hdr->shwa);
	arp_hdr->sprotoa = old_arp->tprotoa;

	memcpy(arp_hdr->thwa, old_arp->shwa, 6);
	arp_hdr->tprotoa = old_arp->sprotoa;

	send_to_link(sizeof(struct ether_hdr) + sizeof(struct arp_hdr), reply, interface);
}

void send_or_queue(char *buf, size_t len, int interface, uint32_t next_hop)
{
	struct arp_table_entry *a = arp_entry(next_hop);

	if (a != NULL) {
		send_with_mac(buf, len, interface, a->mac);
		return;
	}

	put_packet(buf, len, interface, next_hop);

	if (!pending(next_hop)) {
		add_pending(next_hop);
		send_arp_req(next_hop, interface);
	}
}

void handle_arp(char *buf, int interface)
{
	struct arp_hdr *arp_hdr = (struct arp_hdr *)(buf + sizeof(struct ether_hdr));

	add_arp(arp_hdr->sprotoa, arp_hdr->shwa);

	if (ntohs(arp_hdr->opcode) == 1) {
		if (router_ip(arp_hdr->tprotoa)) {
			send_arp_rep(buf, interface);
		}
		return;
	}

	if (ntohs(arp_hdr->opcode) == 2) {
		del_pending(arp_hdr->sprotoa);
		solve_queue(arp_hdr->sprotoa);
	}
}

void send_icmp_err(char *buf, uint8_t type, uint8_t code)
{
	char packet[MAX_PACKET_LEN];
	memset(packet, 0, MAX_PACKET_LEN);

	struct ip_hdr *old_ip = (struct ip_hdr *)(buf + sizeof(struct ether_hdr));
	struct route_table_entry *r = best_route(old_ip->source_addr);

	if (r == NULL) {
		return;
	}

	uint32_t next_hop = r->next_hop;
	if (next_hop == 0) {
		next_hop = old_ip->source_addr;
	}

	struct ether_hdr *eth_hdr = (struct ether_hdr *)packet;
	struct ip_hdr *ip_hdr = (struct ip_hdr *)(packet + sizeof(struct ether_hdr));
	struct icmp_hdr *icmp_hdr = (struct icmp_hdr *)(packet + sizeof(struct ether_hdr) + sizeof(struct ip_hdr));

	eth_hdr->ethr_type = htons(0x0800);

	ip_hdr->ver = 4;
	ip_hdr->ihl = 5;
	ip_hdr->tos = 0;
	ip_hdr->tot_len = htons(sizeof(struct ip_hdr) + sizeof(struct icmp_hdr) + sizeof(struct ip_hdr) + 8);
	ip_hdr->id = htons(1);
	ip_hdr->frag = 0;
	ip_hdr->ttl = 64;
	ip_hdr->proto = 1;
	ip_hdr->source_addr = inet_addr(get_interface_ip(r->interface));
	ip_hdr->dest_addr = old_ip->source_addr;
	ip_hdr->checksum = 0;
	ip_hdr->checksum = htons(checksum((uint16_t *)ip_hdr, sizeof(struct ip_hdr)));

	icmp_hdr->mtype = type;
	icmp_hdr->mcode = code;
	icmp_hdr->un_t.echo_t.id = 0;
	icmp_hdr->un_t.echo_t.seq = 0;

	memcpy((char *)icmp_hdr + sizeof(struct icmp_hdr), old_ip, sizeof(struct ip_hdr) + 8);

	icmp_hdr->check = 0;
	icmp_hdr->check = htons(checksum((uint16_t *)icmp_hdr,
		sizeof(struct icmp_hdr) + sizeof(struct ip_hdr) + 8));

	send_or_queue(packet,
				  sizeof(struct ether_hdr) + sizeof(struct ip_hdr) +
				  sizeof(struct icmp_hdr) + sizeof(struct ip_hdr) + 8,
				  r->interface,
				  next_hop);
}

void send_icmp_reply(char *buf, size_t len, int interface)
{
	struct ether_hdr *eth_hdr = (struct ether_hdr *)buf;
	struct ip_hdr *ip_hdr = (struct ip_hdr *)(buf + sizeof(struct ether_hdr));
	struct icmp_hdr *icmp_hdr = (struct icmp_hdr *)(buf + sizeof(struct ether_hdr) + ip_hdr->ihl * 4);

	uint8_t mac[6];
	memcpy(mac, eth_hdr->ethr_shost, 6);
	get_interface_mac(interface, eth_hdr->ethr_shost);
	memcpy(eth_hdr->ethr_dhost, mac, 6);

	uint32_t ip = ip_hdr->source_addr;
	ip_hdr->source_addr = ip_hdr->dest_addr;
	ip_hdr->dest_addr = ip;
	ip_hdr->ttl = 64;
	ip_hdr->checksum = 0;
	ip_hdr->checksum = htons(checksum((uint16_t *)ip_hdr, ip_hdr->ihl * 4));

	icmp_hdr->mtype = 0;
	icmp_hdr->mcode = 0;
	icmp_hdr->check = 0;
	icmp_hdr->check = htons(checksum((uint16_t *)icmp_hdr, ntohs(ip_hdr->tot_len) - ip_hdr->ihl * 4));

	send_to_link(len, buf, interface);
}

int main(int argc, char *argv[])
{
	char buf[MAX_PACKET_LEN];

	rtable = malloc(sizeof(struct route_table_entry) * 100000);
	DIE(rtable == NULL, "malloc failed");
	rtable_len = read_rtable(argv[1], rtable);

	build_trie();

	arp_table = malloc(sizeof(struct arp_table_entry) * 1000);
	DIE(arp_table == NULL, "malloc failed");
	arp_table_len = 0;

	arp_pending = malloc(sizeof(uint32_t) * 1000);
	DIE(arp_pending == NULL, "malloc failed");
	arp_pending_len = 0;

	q = create_queue();

	init(argv + 2, argc - 2);

	while (1) {
		size_t interface;
		size_t len;

		interface = recv_from_any_link(buf, &len);
		DIE((int)interface < 0, "recv_from_any_link");

		if (len < sizeof(struct ether_hdr)) {
			continue;
		}

		struct ether_hdr *eth_hdr = (struct ether_hdr *)buf;
		uint16_t type = ntohs(eth_hdr->ethr_type);

		if (type == 0x0806) {
			if (len >= sizeof(struct ether_hdr) + sizeof(struct arp_hdr)) {
				handle_arp(buf, interface);
			}
			continue;
		}

		if (type != 0x0800) {
			continue;
		}

		if (len < sizeof(struct ether_hdr) + sizeof(struct ip_hdr)) {
			continue;
		}

		struct ip_hdr *ip_hdr = (struct ip_hdr *)(buf + sizeof(struct ether_hdr));

		if (!good_checksum(ip_hdr)) {
			continue;
		}

		add_arp(ip_hdr->source_addr, eth_hdr->ethr_shost);

		if (router_ip(ip_hdr->dest_addr)) {
			if (ip_hdr->proto == 1) {
				struct icmp_hdr *icmp_hdr =
					(struct icmp_hdr *)(buf + sizeof(struct ether_hdr) + ip_hdr->ihl * 4);

				if (icmp_hdr->mtype == 8) {
					send_icmp_reply(buf, len, interface);
				}
			}
			continue;
		}

		if (ip_hdr->ttl <= 1) {
			send_icmp_err(buf, 11, 0);
			continue;
		}

		struct route_table_entry *r = best_route(ip_hdr->dest_addr);
		if (r == NULL) {
			send_icmp_err(buf, 3, 0);
			continue;
		}

		uint32_t next_hop = r->next_hop;
		if (next_hop == 0) {
			next_hop = ip_hdr->dest_addr;
		}

		ip_hdr->ttl--;
		ip_hdr->checksum = 0;
		ip_hdr->checksum = htons(checksum((uint16_t *)ip_hdr, ip_hdr->ihl * 4));

		send_or_queue(buf, len, r->interface, next_hop);
	}
}

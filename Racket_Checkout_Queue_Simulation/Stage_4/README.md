# Stage 4 — Opening and Closing Counters

Adds `open` and `close` requests to the checkout simulation. Closed counters stop receiving new customers; customers still waiting behind the one being served are redistributed to available counters. The stage retains queue-based processing, time progression, and ordered departure records.

## Files

- `queue.rkt`: queue data type and operations
- `etapa4.rkt`: checkout simulation
- `checker.rkt`: original stage checker

Run from this folder with Racket:

```bash
racket checker.rkt
```

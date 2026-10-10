# Stage 3 — Queue Abstraction and Time Simulation

Replaces list-based customer queues with a dedicated queue data type. Counter operations use the queue interface while the simulation advances time, records customer departures, handles delays, and adds counters when needed.

## Files

- `queue.rkt`: queue data type and operations
- `etapa3.rkt`: checkout simulation
- `checker.rkt`: original stage checker

Run from this folder with Racket:

```bash
racket checker.rkt
```

# Stage 2 — Exit Times and Capacity

Extends each counter with the time until its first customer exits. The simulation applies delays, removes completed customers, chooses counters by service time, and can add counters when the average waiting time exceeds a requested threshold.

## Files

- `etapa2.rkt`: simulation implementation
- `checker.rkt`: original stage checker

Run from this folder with Racket:

```bash
racket checker.rkt
```

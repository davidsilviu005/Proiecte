# Stage 2 — Algebraic Graphs and Partitions

Introduces an algebraic graph type built from empty graphs, nodes, overlays, and connections. Implements graph queries and transformations, then explores list partitions in a separate module.

`AlgebraicGraph.hs` contains the graph representation; `Modular.hs` contains partition helpers. `TestGraph.hs` and `TestPP.hs` are the included checker files.

```bash
ghci -ignore-dot-ghci -v0 TestGraph.hs -e checkAll
```

# Stage 1 — Directed Graphs and Traversal

Represents a directed graph as sets of nodes and edges. Implements graph construction, neighbor queries, node removal, splitting and merging, plus breadth-first and depth-first traversal algorithms.

`StandardGraph.hs` contains the graph operations; `Algorithms.hs` contains traversal functions. `TestGraph.hs` and `TestPP.hs` are the included checker files.

```bash
ghci -ignore-dot-ghci -v0 TestGraph.hs -e checkAll
```

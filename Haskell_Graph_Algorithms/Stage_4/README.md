# Stage 4 — Graph Folds and Stack-Based DFS

Uses `Foldable` and a custom algebraic-graph fold to derive node and edge queries. Separately refines depth-first traversal into an explicit stack-based implementation.

`AlgebraicGraph.hs`, `StandardGraph.hs`, and `Algorithms.hs` contain the implementation. `TestGraph.hs` and `TestPP.hs` are the included checker files.

```bash
ghci -ignore-dot-ghci -v0 TestGraph.hs -e checkAll
```

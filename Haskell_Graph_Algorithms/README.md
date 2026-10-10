# Graph Algorithms and Algebraic Graphs in Haskell

A four-stage functional programming project that explores directed graph operations, graph traversal, algebraic graph representations, modular decomposition, and folds. Each stage is a standalone snapshot with its own checker.

| Stage | Main addition |
| --- | --- |
| [Stage 1](Stage_1/) | Set-based directed graphs, BFS, and DFS |
| [Stage 2](Stage_2/) | Algebraic graph representation and list partitions |
| [Stage 3](Stage_3/) | Graph type classes and modular decomposition |
| [Stage 4](Stage_4/) | Folds over algebraic graphs and stack-based DFS |

Run a stage checker from its folder with GHC/GHCi:

```bash
ghci -ignore-dot-ghci -v0 TestGraph.hs -e checkAll
```

The copied stages pass their included checkers with GHC 9.6.7. Stage 3 has one portfolio-copy fix: its `Modular.hs` import hides a conflicting `Graph` name so the file compiles. Original ZIP submissions, nested archives, and generated files are excluded.

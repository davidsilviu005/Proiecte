# Stage 3 — Graph Abstractions and Modular Decomposition

Extends algebraic graphs with type-class instances and higher-order transformations. The modular-decomposition module evaluates graph modules and partitions and computes a maximal modular partition.

`AlgebraicGraph.hs` and `Modular.hs` contain the implementation. `TestGraph.hs` and `TestPP.hs` are the included checker files. The `Modular.hs` import hides a conflicting `Graph` name that prevented the original copy from compiling; the algorithm code is otherwise unchanged.

```bash
ghci -ignore-dot-ghci -v0 TestGraph.hs -e checkAll
```

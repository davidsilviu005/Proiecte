# C to Assembly Command Converter

This C program reads a small, C-like command language from standard input and prints corresponding assembly-style instructions. It handles assignments, arithmetic and bitwise operations, shifts, and simple `if`, `while`, and `for` constructs.

## Main parts

- `main.c` reads each input line, identifies the operation, and prints the generated instructions.
- Helper functions handle variables, numeric operands, arithmetic, logical operations, comparisons, and loop labels.
- `Makefile` builds the executable named `transpiler` in the parent directory.

## Build and run

From this folder, run `make`, then pass an input file to `../transpiler < input.txt`. The program prints its output to the terminal; it does not create an assembly file automatically.

The accepted syntax is the subset implemented in `main.c`, rather than general C source code.

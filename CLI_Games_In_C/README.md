# Command Line Games in C

This folder contains two terminal games written in C.

## 4 in a Row

`4_in_a_row/` implements a seven-column Connect Four game. The player can face the computer or another player, choose who starts, and place pieces by entering a column number. Its `Makefile` provides `make build`, `make run`, and `make clean` from inside that folder.

## Battleship

`battleship/var_nou.c` implements a terminal Battleship game against the computer. The player chooses a board size, places ships by entering coordinates, selects who starts, and then takes turns firing at coordinates.

Compile it from the `battleship` folder with `gcc var_nou.c -o battleship`, then run the resulting executable. The game prompts and responses are in Romanian.

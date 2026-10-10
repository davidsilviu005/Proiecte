# Chess Project - C++ Engine + Python GUI

This project is a simple chess game built with:

- **C++** for the chess engine
- **Python + Pygame** for the graphical interface

The player controls the **white pieces**, while the engine plays **black**.

## Features

- Legal move generation
- Check validation
- Basic AI using **Minimax + Alpha-Beta pruning**
- Unicode chess pieces in the GUI
- Clean separation between backend and frontend

## Run

You need a C++17 compiler, `make`, Python 3, and Pygame. From this folder, install the Python dependency and build the engine:

```sh
python3 -m pip install pygame
make
make run
```

The provided Makefile uses `g++`, `python3`, and Unix-style commands. Run the GUI from the `chess` folder because it looks for `./chess_engine` there. On Windows, use a compatible shell and toolchain, or adapt the Makefile and engine path for your environment.

The player controls White. Select a piece and then a highlighted destination; the engine responds as Black.

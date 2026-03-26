CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra
ENGINE_SRCS = engine/main.cpp engine/Board.cpp
ENGINE_TARGET = chess_engine

PYTHON = python3

all: $(ENGINE_TARGET)

$(ENGINE_TARGET): $(ENGINE_SRCS) engine/Board.h
	$(CXX) $(CXXFLAGS) $(ENGINE_SRCS) -o $(ENGINE_TARGET)

run: all
	$(PYTHON) gui/main.py

clean:
	rm -f $(ENGINE_TARGET)
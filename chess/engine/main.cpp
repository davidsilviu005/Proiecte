#include "Board.h"
#include <iostream>
#include <string>
#include <vector>

static void printUsage() {
    std::cerr << "Usage:\n";
    std::cerr << "  ./chess_engine best <board64> <side>\n";
    std::cerr << "  ./chess_engine legal <board64> <side>\n";
    std::cerr << "Where:\n";
    std::cerr << "  board64 = 64 characters, row-major, '.' for empty\n";
    std::cerr << "  side    = w or b\n";
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        printUsage();
        return 1;
    }

    std::string mode = argv[1];
    std::string boardStr = argv[2];
    char side = argv[3][0];

    if (boardStr.size() != 64 || (side != 'w' && side != 'b')) {
        printUsage();
        return 1;
    }

    Board board(boardStr, side);

    if (mode == "best") {
        Move mv = findBestMove(board, 3);
        if (mv.fr == -1) {
            std::cout << "none\n";
        } else {
            std::cout << mv.toUCI() << "\n";
        }
    } else if (mode == "legal") {
        auto legal = board.generateLegalMoves(side);
        for (size_t i = 0; i < legal.size(); i++) {
            if (i) std::cout << ' ';
            std::cout << legal[i].toUCI();
        }
        std::cout << "\n";
    } else {
        printUsage();
        return 1;
    }

    return 0;
}
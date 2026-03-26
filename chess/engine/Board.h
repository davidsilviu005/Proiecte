#ifndef BOARD_H
#define BOARD_H

#include <string>
#include <vector>

struct Move {
    int fr, fc, tr, tc;
    char promotion;

    Move(int fr = 0, int fc = 0, int tr = 0, int tc = 0, char promotion = '\0');
    std::string toUCI() const;
};

class Board {
public:
    std::vector<std::string> board;
    char sideToMove; // 'w' or 'b'

    Board();
    Board(const std::string& boardStr, char stm);

    std::string toBoardString() const;

    bool inBounds(int r, int c) const;
    char pieceAt(int r, int c) const;
    void setPiece(int r, int c, char p);

    bool isWhitePiece(char p) const;
    bool isBlackPiece(char p) const;
    bool isOwnPiece(char p, char side) const;
    bool isEnemyPiece(char p, char side) const;

    std::vector<Move> generatePseudoLegalMoves(char side) const;
    std::vector<Move> generateLegalMoves(char side) const;

    bool isSquareAttacked(int r, int c, char bySide) const;
    bool isKingInCheck(char side) const;

    Board makeMove(const Move& mv) const;
    int evaluate() const;

private:
    void addPawnMoves(std::vector<Move>& moves, int r, int c, char side) const;
    void addKnightMoves(std::vector<Move>& moves, int r, int c, char side) const;
    void addSlidingMoves(std::vector<Move>& moves, int r, int c, char side,
                         const std::vector<std::pair<int,int>>& dirs) const;
    void addKingMoves(std::vector<Move>& moves, int r, int c, char side) const;
};

Move findBestMove(const Board& board, int depth);
int negamax(const Board& board, int depth, int alpha, int beta, char side);

#endif
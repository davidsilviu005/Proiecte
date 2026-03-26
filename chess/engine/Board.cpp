#include "Board.h"
#include <algorithm>
#include <cctype>
#include <limits>

Move::Move(int fr, int fc, int tr, int tc, char promotion)
    : fr(fr), fc(fc), tr(tr), tc(tc), promotion(promotion) {}

std::string Move::toUCI() const {
    std::string s;
    s += char('a' + fc);
    s += char('8' - fr);
    s += char('a' + tc);
    s += char('8' - tr);
    if (promotion != '\0') {
        s += char(std::tolower(promotion));
    }
    return s;
}

Board::Board() : board({
    "rnbqkbnr",
    "pppppppp",
    "........",
    "........",
    "........",
    "........",
    "PPPPPPPP",
    "RNBQKBNR"
}), sideToMove('w') {}

Board::Board(const std::string& boardStr, char stm) : board(8, "........"), sideToMove(stm) {
    for (int i = 0; i < 64; i++) {
        board[i / 8][i % 8] = boardStr[i];
    }
}

std::string Board::toBoardString() const {
    std::string s;
    for (const auto& row : board) s += row;
    return s;
}

bool Board::inBounds(int r, int c) const {
    return r >= 0 && r < 8 && c >= 0 && c < 8;
}

char Board::pieceAt(int r, int c) const {
    return board[r][c];
}

void Board::setPiece(int r, int c, char p) {
    board[r][c] = p;
}

bool Board::isWhitePiece(char p) const {
    return p >= 'A' && p <= 'Z';
}

bool Board::isBlackPiece(char p) const {
    return p >= 'a' && p <= 'z';
}

bool Board::isOwnPiece(char p, char side) const {
    return (side == 'w' && isWhitePiece(p)) || (side == 'b' && isBlackPiece(p));
}

bool Board::isEnemyPiece(char p, char side) const {
    return (side == 'w' && isBlackPiece(p)) || (side == 'b' && isWhitePiece(p));
}

void Board::addPawnMoves(std::vector<Move>& moves, int r, int c, char side) const {
    int dir = (side == 'w') ? -1 : 1;
    int startRow = (side == 'w') ? 6 : 1;
    int promoteRow = (side == 'w') ? 0 : 7;
    char promo = (side == 'w') ? 'Q' : 'q';

    int nr = r + dir;
    if (inBounds(nr, c) && pieceAt(nr, c) == '.') {
        if (nr == promoteRow) moves.emplace_back(r, c, nr, c, promo);
        else moves.emplace_back(r, c, nr, c);

        int nr2 = r + 2 * dir;
        if (r == startRow && inBounds(nr2, c) && pieceAt(nr2, c) == '.') {
            moves.emplace_back(r, c, nr2, c);
        }
    }

    for (int dc : {-1, 1}) {
        int nc = c + dc;
        if (inBounds(nr, nc) && isEnemyPiece(pieceAt(nr, nc), side)) {
            if (nr == promoteRow) moves.emplace_back(r, c, nr, nc, promo);
            else moves.emplace_back(r, c, nr, nc);
        }
    }
}

void Board::addKnightMoves(std::vector<Move>& moves, int r, int c, char side) const {
    static const int dr[] = {-2, -2, -1, -1, 1, 1, 2, 2};
    static const int dc[] = {-1, 1, -2, 2, -2, 2, -1, 1};

    for (int i = 0; i < 8; i++) {
        int nr = r + dr[i], nc = c + dc[i];
        if (!inBounds(nr, nc)) continue;
        char target = pieceAt(nr, nc);
        if (target == '.' || isEnemyPiece(target, side)) {
            moves.emplace_back(r, c, nr, nc);
        }
    }
}

void Board::addSlidingMoves(std::vector<Move>& moves, int r, int c, char side,
                            const std::vector<std::pair<int,int>>& dirs) const {
    for (auto [dr, dc] : dirs) {
        int nr = r + dr, nc = c + dc;
        while (inBounds(nr, nc)) {
            char target = pieceAt(nr, nc);
            if (target == '.') {
                moves.emplace_back(r, c, nr, nc);
            } else {
                if (isEnemyPiece(target, side)) {
                    moves.emplace_back(r, c, nr, nc);
                }
                break;
            }
            nr += dr;
            nc += dc;
        }
    }
}

void Board::addKingMoves(std::vector<Move>& moves, int r, int c, char side) const {
    for (int dr = -1; dr <= 1; dr++) {
        for (int dc = -1; dc <= 1; dc++) {
            if (dr == 0 && dc == 0) continue;
            int nr = r + dr, nc = c + dc;
            if (!inBounds(nr, nc)) continue;
            char target = pieceAt(nr, nc);
            if (target == '.' || isEnemyPiece(target, side)) {
                moves.emplace_back(r, c, nr, nc);
            }
        }
    }
}

std::vector<Move> Board::generatePseudoLegalMoves(char side) const {
    std::vector<Move> moves;

    for (int r = 0; r < 8; r++) {
        for (int c = 0; c < 8; c++) {
            char p = pieceAt(r, c);
            if (!isOwnPiece(p, side)) continue;

            char up = std::toupper(p);

            if (up == 'P') {
                addPawnMoves(moves, r, c, side);
            } else if (up == 'N') {
                addKnightMoves(moves, r, c, side);
            } else if (up == 'B') {
                addSlidingMoves(moves, r, c, side, {{-1,-1}, {-1,1}, {1,-1}, {1,1}});
            } else if (up == 'R') {
                addSlidingMoves(moves, r, c, side, {{-1,0}, {1,0}, {0,-1}, {0,1}});
            } else if (up == 'Q') {
                addSlidingMoves(moves, r, c, side, {
                    {-1,-1}, {-1,1}, {1,-1}, {1,1},
                    {-1,0}, {1,0}, {0,-1}, {0,1}
                });
            } else if (up == 'K') {
                addKingMoves(moves, r, c, side);
            }
        }
    }

    return moves;
}

bool Board::isSquareAttacked(int r, int c, char bySide) const {
    int pawnDir = (bySide == 'w') ? -1 : 1;
    int pawnRow = r - pawnDir;

    for (int dc : {-1, 1}) {
        int pc = c + dc;
        if (inBounds(pawnRow, pc)) {
            char p = pieceAt(pawnRow, pc);
            if (bySide == 'w' && p == 'P') return true;
            if (bySide == 'b' && p == 'p') return true;
        }
    }

    static const int knr[] = {-2,-2,-1,-1,1,1,2,2};
    static const int knc[] = {-1,1,-2,2,-2,2,-1,1};
    for (int i = 0; i < 8; i++) {
        int nr = r + knr[i], nc = c + knc[i];
        if (inBounds(nr, nc)) {
            char p = pieceAt(nr, nc);
            if (bySide == 'w' && p == 'N') return true;
            if (bySide == 'b' && p == 'n') return true;
        }
    }

    std::vector<std::pair<int,int>> bishopDirs = {{-1,-1}, {-1,1}, {1,-1}, {1,1}};
    for (auto [dr, dc] : bishopDirs) {
        int nr = r + dr, nc = c + dc;
        while (inBounds(nr, nc)) {
            char p = pieceAt(nr, nc);
            if (p != '.') {
                if (bySide == 'w' && (p == 'B' || p == 'Q')) return true;
                if (bySide == 'b' && (p == 'b' || p == 'q')) return true;
                break;
            }
            nr += dr;
            nc += dc;
        }
    }

    std::vector<std::pair<int,int>> rookDirs = {{-1,0}, {1,0}, {0,-1}, {0,1}};
    for (auto [dr, dc] : rookDirs) {
        int nr = r + dr, nc = c + dc;
        while (inBounds(nr, nc)) {
            char p = pieceAt(nr, nc);
            if (p != '.') {
                if (bySide == 'w' && (p == 'R' || p == 'Q')) return true;
                if (bySide == 'b' && (p == 'r' || p == 'q')) return true;
                break;
            }
            nr += dr;
            nc += dc;
        }
    }

    for (int dr = -1; dr <= 1; dr++) {
        for (int dc = -1; dc <= 1; dc++) {
            if (dr == 0 && dc == 0) continue;
            int nr = r + dr, nc = c + dc;
            if (inBounds(nr, nc)) {
                char p = pieceAt(nr, nc);
                if (bySide == 'w' && p == 'K') return true;
                if (bySide == 'b' && p == 'k') return true;
            }
        }
    }

    return false;
}

bool Board::isKingInCheck(char side) const {
    char king = (side == 'w') ? 'K' : 'k';
    for (int r = 0; r < 8; r++) {
        for (int c = 0; c < 8; c++) {
            if (pieceAt(r, c) == king) {
                return isSquareAttacked(r, c, side == 'w' ? 'b' : 'w');
            }
        }
    }
    return false;
}

std::vector<Move> Board::generateLegalMoves(char side) const {
    std::vector<Move> legal;
    auto pseudo = generatePseudoLegalMoves(side);

    for (const auto& mv : pseudo) {
        Board next = makeMove(mv);
        if (!next.isKingInCheck(side)) {
            legal.push_back(mv);
        }
    }

    return legal;
}

Board Board::makeMove(const Move& mv) const {
    Board next = *this;
    char piece = next.pieceAt(mv.fr, mv.fc);
    next.setPiece(mv.fr, mv.fc, '.');
    next.setPiece(mv.tr, mv.tc, (mv.promotion != '\0') ? mv.promotion : piece);
    next.sideToMove = (sideToMove == 'w') ? 'b' : 'w';
    return next;
}

int Board::evaluate() const {
    auto value = [](char p) -> int {
        switch (std::toupper(p)) {
            case 'P': return 100;
            case 'N': return 320;
            case 'B': return 330;
            case 'R': return 500;
            case 'Q': return 900;
            case 'K': return 20000;
            default: return 0;
        }
    };

    int score = 0;
    for (int r = 0; r < 8; r++) {
        for (int c = 0; c < 8; c++) {
            char p = pieceAt(r, c);
            if (p == '.') continue;
            if (isWhitePiece(p)) score += value(p);
            else score -= value(p);
        }
    }
    return score;
}

int negamax(const Board& board, int depth, int alpha, int beta, char side) {
    auto legal = board.generateLegalMoves(side);

    if (depth == 0 || legal.empty()) {
        if (legal.empty()) {
            if (board.isKingInCheck(side)) {
                return -100000 + (3 - depth);
            }
            return 0;
        }
        int eval = board.evaluate();
        return (side == 'w') ? eval : -eval;
    }

    int best = std::numeric_limits<int>::min();

    for (const auto& mv : legal) {
        Board next = board.makeMove(mv);
        int score = -negamax(next, depth - 1, -beta, -alpha, next.sideToMove);

        best = std::max(best, score);
        alpha = std::max(alpha, score);
        if (alpha >= beta) break;
    }

    return best;
}

Move findBestMove(const Board& board, int depth) {
    auto legal = board.generateLegalMoves(board.sideToMove);
    if (legal.empty()) return Move(-1, -1, -1, -1);

    Move bestMove = legal[0];
    int bestScore = std::numeric_limits<int>::min();
    int alpha = std::numeric_limits<int>::min() / 2;
    int beta = std::numeric_limits<int>::max() / 2;

    for (const auto& mv : legal) {
        Board next = board.makeMove(mv);
        int score = -negamax(next, depth - 1, -beta, -alpha, next.sideToMove);
        if (score > bestScore) {
            bestScore = score;
            bestMove = mv;
        }
        alpha = std::max(alpha, score);
    }

    return bestMove;
}
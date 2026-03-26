import sys
import subprocess
import pygame

WINDOW_SIZE = 640
SQUARE_SIZE = WINDOW_SIZE // 8
FPS = 60

LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT = (246, 246, 105)
MOVE_DOT = (80, 80, 80)
TEXT_COLOR = (20, 20, 20)

PIECE_TO_UNICODE = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
    '.': ''
}

ENGINE_PATH = "./chess_engine"

class ChessGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 40))
        pygame.display.set_caption("Chess: C++ Engine + Python GUI")
        self.clock = pygame.time.Clock()

        self.piece_font = pygame.font.SysFont("DejaVu Sans", 46)
        self.info_font = pygame.font.SysFont("Arial", 24)

        self.board = [
            list("rnbqkbnr"),
            list("pppppppp"),
            list("........"),
            list("........"),
            list("........"),
            list("........"),
            list("PPPPPPPP"),
            list("RNBQKBNR")
        ]

        self.selected = None
        self.legal_moves_cache = []
        self.info_text = "You are White"
        self.game_over = False

    def board_string(self):
        return ''.join(''.join(row) for row in self.board)

    def get_engine_legal_moves(self, side):
        try:
            result = subprocess.check_output(
                [ENGINE_PATH, "legal", self.board_string(), side],
                text=True
            ).strip()
            if not result:
                return []
            return result.split()
        except Exception as e:
            self.info_text = f"Engine error: {e}"
            return []

    def get_engine_best_move(self, side):
        try:
            result = subprocess.check_output(
                [ENGINE_PATH, "best", self.board_string(), side],
                text=True
            ).strip()
            return result
        except Exception as e:
            self.info_text = f"Engine error: {e}"
            return "none"

    def coord_to_square(self, row, col):
        return chr(ord('a') + col) + str(8 - row)

    def square_to_coord(self, sq):
        col = ord(sq[0]) - ord('a')
        row = 8 - int(sq[1])
        return row, col

    def parse_move(self, uci):
        fr = self.square_to_coord(uci[:2])
        to = self.square_to_coord(uci[2:4])
        promo = uci[4] if len(uci) == 5 else None
        return fr, to, promo

    def apply_move(self, uci):
        (fr, fc), (tr, tc), promo = self.parse_move(uci)
        piece = self.board[fr][fc]
        self.board[fr][fc] = '.'

        if promo:
            piece = promo.upper() if piece.isupper() else promo.lower()

        self.board[tr][tc] = piece

    def is_white_piece(self, p):
        return 'A' <= p <= 'Z'

    def legal_moves_from_selected(self):
        if self.selected is None:
            return []
        sr, sc = self.selected
        from_sq = self.coord_to_square(sr, sc)
        return [mv for mv in self.legal_moves_cache if mv.startswith(from_sq)]

    def draw(self):
        self.screen.fill((230, 230, 230))

        for row in range(8):
            for col in range(8):
                color = LIGHT if (row + col) % 2 == 0 else DARK
                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

        if self.selected is not None:
            sr, sc = self.selected
            rect = pygame.Rect(sc * SQUARE_SIZE, sr * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(self.screen, HIGHLIGHT, rect)

            for mv in self.legal_moves_from_selected():
                (_, _), (tr, tc), _ = self.parse_move(mv)
                center = (tc * SQUARE_SIZE + SQUARE_SIZE // 2, tr * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(self.screen, MOVE_DOT, center, 10)

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece != '.':
                    symbol = PIECE_TO_UNICODE[piece]
                    text = self.piece_font.render(symbol, True, TEXT_COLOR)
                    rect = text.get_rect(center=(
                        col * SQUARE_SIZE + SQUARE_SIZE // 2,
                        row * SQUARE_SIZE + SQUARE_SIZE // 2
                    ))
                    self.screen.blit(text, rect)

        info_surface = self.info_font.render(self.info_text, True, (0, 0, 0))
        self.screen.blit(info_surface, (10, WINDOW_SIZE + 8))

        pygame.display.flip()

    def player_turn(self, row, col):
        if self.game_over:
            return

        if self.selected is None:
            piece = self.board[row][col]
            if self.is_white_piece(piece):
                self.selected = (row, col)
        else:
            sr, sc = self.selected
            candidate = self.coord_to_square(sr, sc) + self.coord_to_square(row, col)

            matched_move = None
            for mv in self.legal_moves_from_selected():
                if mv[:4] == candidate:
                    matched_move = mv
                    break

            if matched_move:
                self.apply_move(matched_move)
                self.selected = None
                self.after_player_move()
            else:
                if self.is_white_piece(self.board[row][col]):
                    self.selected = (row, col)
                else:
                    self.selected = None

    def after_player_move(self):
        black_legal = self.get_engine_legal_moves('b')
        if not black_legal:
            self.game_over = True
            self.info_text = "Game over"
            return

        self.info_text = "Engine is thinking..."
        self.draw()

        best = self.get_engine_best_move('b')
        if best == "none":
            self.game_over = True
            self.info_text = "Game over"
            return

        self.apply_move(best)

        white_legal = self.get_engine_legal_moves('w')
        if not white_legal:
            self.game_over = True
            self.info_text = "Game over"
            self.legal_moves_cache = []
        else:
            self.legal_moves_cache = white_legal
            self.info_text = f"Engine played: {best}"

    def run(self):
        self.legal_moves_cache = self.get_engine_legal_moves('w')
        if not self.legal_moves_cache:
            self.info_text = "No legal moves at start"
            self.game_over = True

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    if my < WINDOW_SIZE:
                        col = mx // SQUARE_SIZE
                        row = my // SQUARE_SIZE
                        self.player_turn(row, col)

            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    app = ChessGUI()
    app.run()
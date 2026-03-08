import tkinter as tk
from tkinter import messagebox, simpledialog
import random

COLORS = {
    "bg": "#1E1E2F",
    "board_bg": "#25253A",
    "btn_bg": "#30304A",
    "btn_hover": "#3E3E5E",
    "btn_active": "#4ECDC4",
    "x_color": "#FF6B6B",
    "o_color": "#4ECDC4",
    "status_text": "#F7FFF7",
    "status_bg": "#1E1E2F",
    "reset_bg": "#4ECDC4",
    "reset_fg": "#1E1E2F",
}

current_player = "X"
board = [["" for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
game_over = False
mode = None
difficulty = None
human_starts = True
pvp_start_symbol = "X"
score_x = 0
score_o = 0
score_draw = 0

def evaluate_board(b):
    for row in range(3):
        if b[row][0] != "" and b[row][0] == b[row][1] == b[row][2]:
            return b[row][0]
    for col in range(3):
        if b[0][col] != "" and b[0][col] == b[1][col] == b[2][col]:
            return b[0][col]
    if b[0][0] != "" and b[0][0] == b[1][1] == b[2][2]:
        return b[0][0]
    if b[0][2] != "" and b[0][2] == b[1][1] == b[2][0]:
        return b[0][2]
    if all(b[r][c] != "" for r in range(3) for c in range(3)):
        return "Draw"
    return None

def check_winner():
    return evaluate_board(board)

def get_available_moves(b=None):
    if b is None:
        b = board
    return [(r, c) for r in range(3) for c in range(3) if b[r][c] == ""]

def minimax(b, is_maximizing):
    winner = evaluate_board(b)
    if winner is not None:
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        else:
            return 0
    if is_maximizing:
        best_score = -999
        for (r, c) in get_available_moves(b):
            b[r][c] = "O"
            score = minimax(b, False)
            b[r][c] = ""
            if score > best_score:
                best_score = score
        return best_score
    else:
        best_score = 999
        for (r, c) in get_available_moves(b):
            b[r][c] = "X"
            score = minimax(b, True)
            b[r][c] = ""
            if score < best_score:
                best_score = score
        return best_score

def best_move_impossible():
    best_score = -999
    best_move = None
    for (r, c) in get_available_moves():
        board[r][c] = "O"
        score = minimax(board, False)
        board[r][c] = ""
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move

def best_move_hard():
    moves = get_available_moves()
    for (r, c) in moves:
        board[r][c] = "O"
        if evaluate_board(board) == "O":
            board[r][c] = ""
            return (r, c)
        board[r][c] = ""
    for (r, c) in moves:
        board[r][c] = "X"
        if evaluate_board(board) == "X":
            board[r][c] = ""
            return (r, c)
        board[r][c] = ""
    if board[1][1] == "":
        return (1, 1)
    return random.choice(moves) if moves else None

def best_move_easy():
    moves = get_available_moves()
    return random.choice(moves) if moves else None

def update_score_label():
    if mode == "BOT":
        score_label["text"] = f"You (X): {score_x}   Bot (O): {score_o}   Draws: {score_draw}"
    else:
        score_label["text"] = f"X wins: {score_x}   O wins: {score_o}   Draws: {score_draw}"

def end_game(winner):
    global game_over, score_x, score_o, score_draw
    game_over = True
    if winner == "Draw":
        score_draw += 1
        status_label["text"] = "It's a draw!"
        update_score_label()
        messagebox.showinfo("Game Over", "It's a draw!")
        return
    if winner == "X":
        score_x += 1
    else:
        score_o += 1
    update_score_label()
    if mode == "BOT":
        msg = "You win! 🎉" if winner == "X" else "Bot wins! 🤖"
    else:
        msg = f"Player {winner} wins!"
    status_label["text"] = msg
    messagebox.showinfo("Game Over", msg)

def bot_move():
    global current_player, game_over
    if game_over:
        return
    if difficulty == "impossible":
        move = best_move_impossible()
    elif difficulty == "hard":
        move = best_move_hard()
    else:
        move = best_move_easy()
    if move is None:
        return
    r, c = move
    board[r][c] = "O"
    btn = buttons[r][c]
    btn["text"] = "O"
    btn["state"] = "disabled"
    btn["bg"] = COLORS["btn_bg"]
    btn["fg"] = COLORS["o_color"]
    winner = check_winner()
    if winner is not None:
        end_game(winner)
    else:
        current_player = "X"
        status_label["text"] = "Your turn (X)" if mode == "BOT" else "Player X's turn"

def on_click(row, col):
    global current_player, game_over
    if game_over:
        return
    if mode == "BOT" and current_player == "O":
        return
    if board[row][col] != "":
        return
    board[row][col] = current_player
    btn = buttons[row][col]
    btn["text"] = current_player
    btn["state"] = "disabled"
    btn["bg"] = COLORS["btn_bg"]
    btn["fg"] = COLORS["x_color"] if current_player == "X" else COLORS["o_color"]
    winner = check_winner()
    if winner is not None:
        end_game(winner)
    else:
        if mode == "BOT":
            current_player = "O"
            status_label["text"] = "Bot's turn (O)..."
            root.after(150, bot_move)
        else:
            current_player = "O" if current_player == "X" else "X"
            status_label["text"] = f"Player {current_player}'s turn"

def reset_game():
    global current_player, board, game_over
    board = [["" for _ in range(3)] for _ in range(3)]
    game_over = False
    for r in range(3):
        for c in range(3):
            btn = buttons[r][c]
            btn["text"] = ""
            btn["state"] = "normal"
            btn["bg"] = COLORS["btn_bg"]
            btn["fg"] = "white"
    if mode == "BOT":
        if human_starts:
            current_player = "X"
            status_label["text"] = "You (X) vs Bot (O) – your turn"
        else:
            current_player = "O"
            status_label["text"] = "Bot (O) starts..."
            root.after(300, bot_move)
    else:
        current_player = pvp_start_symbol
        status_label["text"] = f"Player {current_player}'s turn"

def on_enter(btn):
    if btn["state"] == "normal" and btn["text"] == "":
        btn["bg"] = COLORS["btn_hover"]

def on_leave(btn):
    if btn["state"] == "normal" and btn["text"] == "":
        btn["bg"] = COLORS["btn_bg"]

root = tk.Tk()
root.title("Tic Tac Toe")
root.configure(bg=COLORS["bg"])
window_width = 340
window_height = 460
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coord = int((screen_width / 2) - (window_width / 2))
y_coord = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")

score_label = tk.Label(root, text="", font=("Arial", 12, "bold"), bg=COLORS["status_bg"], fg=COLORS["status_text"])
score_label.pack(pady=(10, 5))

board_frame = tk.Frame(root, bg=COLORS["board_bg"], padx=10, pady=10)
board_frame.pack(pady=10)

for r in range(3):
    for c in range(3):
        btn = tk.Button(board_frame, text="", font=("Arial", 32, "bold"), width=3, height=1,
                        bg=COLORS["btn_bg"], fg="white", activebackground=COLORS["btn_active"],
                        activeforeground="black", borderwidth=0, relief="flat",
                        command=lambda row=r, col=c: on_click(row, col))
        btn.grid(row=r, column=c, padx=5, pady=5)
        btn.bind("<Enter>", lambda e, b=btn: on_enter(b))
        btn.bind("<Leave>", lambda e, b=btn: on_leave(b))
        buttons[r][c] = btn

status_label = tk.Label(root, text="", font=("Arial", 14), bg=COLORS["status_bg"], fg=COLORS["status_text"])
status_label.pack(pady=(5, 10))

reset_button = tk.Button(root, text="Reset", font=("Arial", 12, "bold"), bg=COLORS["reset_bg"],
                         fg=COLORS["reset_fg"], activebackground=COLORS["btn_active"],
                         activeforeground="black", relief="flat", padx=20, pady=5, command=reset_game)
reset_button.pack(pady=5)

def choose_mode_and_difficulty():
    global mode, difficulty, human_starts, pvp_start_symbol, current_player
    answer = messagebox.askquestion("Game Mode", "Do you want to play against the computer?\n\nYes = vs Bot\nNo = 2 Players", icon="question")
    if answer == "yes":
        mode = "BOT"
        while True:
            diff = simpledialog.askstring("Difficulty", "Choose difficulty:\n- easy\n- hard\n- impossible", parent=root)
            if diff is None:
                difficulty = "easy"
                break
            diff = diff.strip().lower()
            if diff in ("easy", "hard", "impossible"):
                difficulty = diff
                break
            else:
                messagebox.showerror("Invalid choice", "Please type: easy, hard, or impossible.")
        ans_start = messagebox.askquestion("Who starts?", "Do you want to start first?\n\nYes = You (X)\nNo = Bot (O)", icon="question")
        human_starts = (ans_start == "yes")
        if human_starts:
            current_player = "X"
            status_label["text"] = "You (X) vs Bot (O) – your turn"
        else:
            current_player = "O"
            status_label["text"] = "Bot (O) starts..."
            root.after(300, bot_move)
    else:
        mode = "PVP"
        difficulty = None
        while True:
            sym = simpledialog.askstring("Who starts?", "Who should start first? X or O?", parent=root)
            if sym is None:
                pvp_start_symbol = "X"
                break
            sym = sym.strip().upper()
            if sym in ("X", "O"):
                pvp_start_symbol = sym
                break
            else:
                messagebox.showerror("Invalid choice", "Please type: X or O.")
        current_player = pvp_start_symbol
        status_label["text"] = f"Player {current_player}'s turn"
    update_score_label()

root.after(100, choose_mode_and_difficulty)
root.mainloop()

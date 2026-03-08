import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import leaderboard_core as lb

SIZE = 5  # fixed 5x5 board

COLORS = {
    0: ("#3c3c3c", "#cdc1b4"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
    4096: ("#3c3c3c", "#f9f6f2"),
    8192: ("#3c3c3c", "#f9f6f2"),
}

board = [[0] * SIZE for _ in range(SIZE)]
score = 0
best_score = 0
game_over = False
score_saved = False
PLAYER_NAME = "Player"

root = tk.Tk()
root.title("2048 game")
root.configure(bg="#1e1e2f")

top_frame = tk.Frame(root, bg="#1e1e2f")
top_frame.pack(pady=10)

score_label = tk.Label(
    top_frame,
    text="Score: 0",
    font=("Arial", 14, "bold"),
    bg="#1e1e2f",
    fg="#f8f8f2",
)
score_label.pack(side="left", padx=10)

best_label = tk.Label(
    top_frame,
    text="Best: 0",
    font=("Arial", 14, "bold"),
    bg="#1e1e2f",
    fg="#f8f8f2",
)
best_label.pack(side="right", padx=10)

board_frame = tk.Frame(root, bg="#bbada0", bd=5, relief="ridge")
board_frame.pack(padx=10, pady=(0, 10))

tiles = [[None] * SIZE for _ in range(SIZE)]


def reset_board():
    global board, score, game_over, score_saved
    board = [[0] * SIZE for _ in range(SIZE)]
    score = 0
    game_over = False
    score_saved = False
    add_random_tile()
    add_random_tile()
    update_ui()


def add_random_tile():
    empty = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] == 0]
    if not empty:
        return
    r, c = random.choice(empty)
    board[r][c] = 4 if random.random() < 0.1 else 2


def score_add(val):
    global score, best_score
    score += val
    if score > best_score:
        best_score = score


def compress_line(line):
    new = [v for v in line if v != 0]
    merged = []
    gained = 0
    i = 0
    while i < len(new):
        if i + 1 < len(new) and new[i] == new[i + 1]:
            val = new[i] * 2
            merged.append(val)
            gained += val
            i += 2
        else:
            merged.append(new[i])
            i += 1
    merged += [0] * (SIZE - len(merged))
    return merged, gained


def move_left():
    global board
    moved = False
    total_gain = 0
    new_board = []
    for r in range(SIZE):
        new_row, gain = compress_line(board[r])
        total_gain += gain
        if new_row != board[r]:
            moved = True
        new_board.append(new_row)
    board = new_board
    if moved:
        score_add(total_gain)
    return moved


def move_right():
    global board
    moved = False
    total_gain = 0
    new_board = []
    for r in range(SIZE):
        reversed_row = list(reversed(board[r]))
        new_row, gain = compress_line(reversed_row)
        new_row = list(reversed(new_row))
        total_gain += gain
        if new_row != board[r]:
            moved = True
        new_board.append(new_row)
    board = new_board
    if moved:
        score_add(total_gain)
    return moved


def move_up():
    global board
    moved = False
    total_gain = 0
    new_board = [[0] * SIZE for _ in range(SIZE)]
    for c in range(SIZE):
        col = [board[r][c] for r in range(SIZE)]
        new_col, gain = compress_line(col)
        total_gain += gain
        for r in range(SIZE):
            new_board[r][c] = new_col[r]
        if new_col != col:
            moved = True
    board = new_board
    if moved:
        score_add(total_gain)
    return moved


def move_down():
    global board
    moved = False
    total_gain = 0
    new_board = [[0] * SIZE for _ in range(SIZE)]
    for c in range(SIZE):
        col = [board[r][c] for r in range(SIZE)]
        reversed_col = list(reversed(col))
        new_col, gain = compress_line(reversed_col)
        new_col = list(reversed(new_col))
        total_gain += gain
        for r in range(SIZE):
            new_board[r][c] = new_col[r]
        if new_col != col:
            moved = True
    board = new_board
    if moved:
        score_add(total_gain)
    return moved


def is_game_over():
    for r in range(SIZE):
        for c in range(SIZE):
            v = board[r][c]
            if v == 0:
                return False
            if c + 1 < SIZE and v == board[r][c + 1]:
                return False
            if r + 1 < SIZE and v == board[r + 1][c]:
                return False
    return True


def update_ui():
    score_label.config(text=f"Score: {score}")
    best_label.config(text=f"Best: {best_score}")
    for r in range(SIZE):
        for c in range(SIZE):
            value = board[r][c]
            bg, fg = COLORS.get(value, ("#3c3c3c", "#f9f6f2"))
            label = tiles[r][c]
            text = str(value) if value != 0 else ""
            label.config(text=text, bg=bg, fg=fg)


def save_score_if_needed():
    global score_saved
    if score_saved:
        return
    if PLAYER_NAME and score > 0:
        lb.add_score(
            "2048_5x5",
            PLAYER_NAME,
            score,
            extra={"best_session": best_score},
        )
    score_saved = True


def finish_game():
    global game_over
    if game_over:
        return
    game_over = True
    save_score_if_needed()
    messagebox.showinfo("Game Finished", f"Your score: {score}")


def move(direction):
    global game_over
    if game_over:
        return

    if direction == "Left":
        moved = move_left()
    elif direction == "Right":
        moved = move_right()
    elif direction == "Up":
        moved = move_up()
    elif direction == "Down":
        moved = move_down()
    else:
        return

    if moved:
        add_random_tile()
        update_ui()
        if is_game_over():
            game_over = True
            save_score_if_needed()
            messagebox.showinfo("Game Over", f"No more moves!\nYour score: {score}")


def on_key(event):
    key = event.keysym
    mapping = {
        "Left": "Left",
        "Right": "Right",
        "Up": "Up",
        "Down": "Down",
        "a": "Left",
        "A": "Left",
        "d": "Right",
        "D": "Right",
        "w": "Up",
        "W": "Up",
        "s": "Down",
        "S": "Down",
    }
    if key in mapping:
        move(mapping[key])


def ask_player_name():
    global PLAYER_NAME
    name = simpledialog.askstring(
        "Player Name",
        "Enter your name:",
        parent=root,
    )
    if not name:
        name = "Player"
    PLAYER_NAME = name


for r in range(SIZE):
    for c in range(SIZE):
        lbl = tk.Label(
            board_frame,
            text="",
            width=4,
            height=2,
            font=("Arial", 18, "bold"),
            bg="#3c3c3c",
            fg="#cdc1b4",
            bd=4,
            relief="ridge",
        )
        lbl.grid(row=r, column=c, padx=3, pady=3)
        tiles[r][c] = lbl

buttons_frame = tk.Frame(root, bg="#1e1e2f")
buttons_frame.pack(pady=(0, 10))

btn_reset = tk.Button(
    buttons_frame,
    text="New Game",
    font=("Arial", 12, "bold"),
    bg="#8bc34a",
    fg="#1e1e2f",
    bd=0,
    padx=20,
    pady=5,
    command=reset_board,
)
btn_reset.pack(side="left", padx=5)

btn_finish = tk.Button(
    buttons_frame,
    text="Finish",
    font=("Arial", 12, "bold"),
    bg="#ffb86c",
    fg="#1e1e2f",
    bd=0,
    padx=20,
    pady=5,
    command=finish_game,
)
btn_finish.pack(side="left", padx=5)

root.bind("<Key>", on_key)

ask_player_name()
reset_board()

window_w = 120 + SIZE * 80
window_h = 200 + SIZE * 80
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
x = int(sw / 2 - window_w / 2)
y = int(sh / 2 - window_h / 2)
root.geometry(f"{window_w}x{window_h}+{x}+{y}")

root.mainloop()

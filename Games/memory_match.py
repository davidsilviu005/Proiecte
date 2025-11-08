import tkinter as tk
import random
import time
from tkinter import simpledialog
import leaderboard_core as lb

DIFFICULTIES = {
    "Easy": (4, 4),   # 16 cells -> 8 pairs
    "Medium": (4, 6), # 24 cells -> 12 pairs
    "Hard": (6, 6),   # 36 cells -> 18 pairs
}

SYMBOLS = [
    "🍎", "🍌", "🍇", "🍓", "🍒", "🍉", "🥝", "🍍",
    "🍑", "🥥", "🥕", "🍆", "🌽", "🍋", "🥦", "🍊",
    "🍐", "🍈"
]

current_difficulty = "Easy"
ROWS, COLS = DIFFICULTIES[current_difficulty]

buttons = []
values = []

first_pick = None
lock_input = False
pairs_found = 0
moves = 0  # attempts

start_time = None
timer_running = False
score_saved = False
PLAYER_NAME = "Player"

root = tk.Tk()
root.title("Memory Match")
root.configure(bg="#1e1e2f")

top_frame = tk.Frame(root, bg="#1e1e2f")
top_frame.pack(pady=(8, 4))

status_label = tk.Label(
    top_frame,
    text="Find all pairs!",
    font=("Arial", 14, "bold"),
    bg="#1e1e2f",
    fg="#f8f8f2",
)
status_label.pack(side="left", padx=10)

timer_label = tk.Label(
    top_frame,
    text="Time: 0s",
    font=("Arial", 12, "bold"),
    bg="#1e1e2f",
    fg="#f8f8f2",
)
timer_label.pack(side="right", padx=10)

stats_frame = tk.Frame(root, bg="#1e1e2f")
stats_frame.pack(pady=(0, 4))

attempts_label = tk.Label(
    stats_frame,
    text="Attempts: 0",
    font=("Arial", 12, "bold"),
    bg="#1e1e2f",
    fg="#f8f8f2",
)
attempts_label.pack()

controls_frame = tk.Frame(root, bg="#1e1e2f")
controls_frame.pack(pady=(0, 4))


def set_difficulty(level):
    global current_difficulty, ROWS, COLS
    current_difficulty = level
    ROWS, COLS = DIFFICULTIES[level]
    create_board()
    reset_game()


btn_style = {
    "font": ("Arial", 10, "bold"),
    "bg": "#6272a4",
    "fg": "#f8f8f2",
    "activebackground": "#8be9fd",
    "activeforeground": "#1e1e2f",
    "bd": 0,
    "padx": 10,
    "pady": 4,
}

tk.Button(
    controls_frame,
    text="Easy",
    command=lambda: set_difficulty("Easy"),
    **btn_style,
).pack(side="left", padx=5)

tk.Button(
    controls_frame,
    text="Medium",
    command=lambda: set_difficulty("Medium"),
    **btn_style,
).pack(side="left", padx=5)

tk.Button(
    controls_frame,
    text="Hard",
    command=lambda: set_difficulty("Hard"),
    **btn_style,
).pack(side="left", padx=5)


def new_game():
    reset_game()


btn_new = tk.Button(
    controls_frame,
    text="New Game",
    font=("Arial", 10, "bold"),
    bg="#8bc34a",
    fg="#1e1e2f",
    activebackground="#a5d6a7",
    activeforeground="#1e1e2f",
    bd=0,
    padx=10,
    pady=4,
    command=new_game,
)
btn_new.pack(side="left", padx=10)

board_frame = tk.Frame(root, bg="#25253a", padx=10, pady=10)
board_frame.pack(padx=10, pady=10)


def create_board():
    global buttons, values
    for w in board_frame.winfo_children():
        w.destroy()

    buttons = [[None for _ in range(COLS)] for _ in range(ROWS)]
    values = [[None for _ in range(COLS)] for _ in range(ROWS)]

    for r in range(ROWS):
        for c in range(COLS):
            b = tk.Button(
                board_frame,
                text="",
                width=4,
                height=2,
                font=("Arial", 20, "bold"),
                bg="#30304a",
                fg="#f8f8f2",
                command=lambda row=r, col=c: on_click(row, col),
            )
            b.grid(row=r, column=c, padx=4, pady=4)
            buttons[r][c] = b

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    ww = 80 + COLS * 60
    wh = 160 + ROWS * 70
    x = int(sw / 2 - ww / 2)
    y = int(sh / 2 - wh / 2)
    root.geometry(f"{ww}x{wh}+{x}+{y}")



def start_timer():
    global start_time, timer_running
    start_time = time.time()
    timer_running = True
    update_timer()


def update_timer():
    if not timer_running or start_time is None:
        return
    elapsed = int(time.time() - start_time)
    timer_label.config(text=f"Time: {elapsed}s")
    root.after(500, update_timer)


def reset_game():
    global values, first_pick, lock_input, pairs_found, moves, timer_running, score_saved

    pairs_needed = (ROWS * COLS) // 2
    if pairs_needed > len(SYMBOLS):
        raise ValueError("Not enough SYMBOLS for this difficulty!")

    chosen = SYMBOLS[:pairs_needed]
    items = chosen * 2
    random.shuffle(items)

    idx = 0
    for r in range(ROWS):
        for c in range(COLS):
            values[r][c] = items[idx]
            idx += 1

    first_pick = None
    lock_input = False
    pairs_found = 0
    moves = 0
    score_saved = False
    status_label.config(text=f"{current_difficulty} – Find all pairs!")
    timer_label.config(text="Time: 0s")
    attempts_label.config(text="Attempts: 0")
    timer_running = False
    start_timer()

    for r in range(ROWS):
        for c in range(COLS):
            buttons[r][c].config(text="", state="normal", bg="#30304a")


def on_click(r, c):
    global first_pick, lock_input, pairs_found, moves
    if lock_input:
        return

    btn = buttons[r][c]
    if btn["text"] != "":
        return

    btn.config(text=values[r][c], bg="#44475a")

    if first_pick is None:
        first_pick = (r, c)
    else:
        moves += 1
        attempts_label.config(text=f"Attempts: {moves}")

        r1, c1 = first_pick
        first_btn = buttons[r1][c1]
        if values[r1][c1] == values[r][c]:
            first_btn.config(bg="#50fa7b", state="disabled")
            btn.config(bg="#50fa7b", state="disabled")
            pairs_found += 1
            first_pick = None
            if pairs_found == (ROWS * COLS) // 2:
                end_game()
        else:
            lock_input = True

            def hide():
                global lock_input
                first_btn.config(text="", bg="#30304a")
                btn.config(text="", bg="#30304a")
                lock_input = False

            root.after(700, hide)
            first_pick = None


def save_score_if_needed():
    global score_saved
    if score_saved:
        return
    if start_time is None or moves == 0:
        return

    elapsed = int(time.time() - start_time)
    # Scor mai mare = mai bine (timp mai mic + mai puține încercări)
    raw = 10000 - (elapsed * 50 + moves * 20)
    score_value = max(1, raw)

    lb.add_score(
        "memory_match",
        PLAYER_NAME,
        score_value,
        extra={
            "difficulty": current_difficulty,
            "time_s": elapsed,
            "attempts": moves,
        },
    )
    score_saved = True


def end_game():
    global timer_running
    timer_running = False
    elapsed = int(time.time() - start_time) if start_time else 0
    save_score_if_needed()
    status_label.config(
        text=f"You won {current_difficulty} in {moves} attempts and {elapsed}s! 🎉"
    )


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


ask_player_name()
create_board()
reset_game()

root.mainloop()

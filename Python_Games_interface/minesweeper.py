import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
import leaderboard_core as lb

ROWS = 0
COLS = 0
MINES = 0

COLORS = {
    "bg": "#1E1E2F",
    "board_bg": "#25253A",
    "cell_hidden": "#30304A",
    "cell_revealed": "#44475A",
    "cell_mine": "#FF5555",
    "cell_flag": "#FFB86C",
    "text": "#F8F8F2",
    "status_bg": "#1E1E2F",
    "status_text": "#F8F8F2",
    "reset_bg": "#50FA7B",
    "reset_fg": "#1E1E2F",
}

NUMBER_COLORS = {
    1: "#8BE9FD",
    2: "#50FA7B",
    3: "#FFB86C",
    4: "#BD93F9",
    5: "#FF79C6",
    6: "#69FF94",
    7: "#F1FA8C",
    8: "#FFFFFF",
}

root = tk.Tk()
root.title("Minesweeper")
root.configure(bg=COLORS["bg"])

cells = []
buttons = []
game_over = False
first_click = True
mines_left = 0
start_time = None
timer_running = False
best_time = None
difficulty = "easy"
PLAYER_NAME = "Player"


def format_time(t):
    if t is None:
        return "—"
    t = int(t)
    m = t // 60
    s = t % 60
    return f"{m:02d}:{s:02d}"


def set_difficulty():
    global ROWS, COLS, MINES, difficulty
    while True:
        ans = simpledialog.askstring(
            "Difficulty",
            "Choose difficulty:\n- easy\n- medium\n- hard",
            parent=root,
        )
        if ans is None:
            ans = "easy"
        ans = ans.strip().lower()
        if ans in ("easy", "medium", "hard"):
            difficulty = ans
            break
        else:
            messagebox.showerror("Invalid choice", "Please type: easy, medium, or hard.")

    if difficulty == "easy":
        ROWS, COLS, MINES = 8, 7, 10
    elif difficulty == "medium":
        ROWS, COLS, MINES = 15, 15, 40
    else:  # smaller hard board now
        ROWS, COLS, MINES = 20, 20, 80


def create_board():
    global cells, buttons, game_over, first_click, mines_left, start_time, timer_running

    game_over = False
    first_click = True
    mines_left = MINES
    start_time = None
    timer_running = False

    status_label.config(text=f"Mines: {mines_left}")
    timer_label.config(text="Time: 0    Best: " + format_time(best_time))

    for row_buttons in buttons:
        for b in row_buttons:
            b.destroy()
    cells.clear()
    buttons.clear()

    board_frame.configure(bg=COLORS["board_bg"])

    for r in range(ROWS):
        row_cells = []
        row_buttons = []
        for c in range(COLS):
            cell = {
                "is_mine": False,
                "is_revealed": False,
                "is_flagged": False,
                "neighbor_mines": 0,
            }
            row_cells.append(cell)

            btn = tk.Button(
                board_frame,
                width=2,
                height=1,
                bg=COLORS["cell_hidden"],
                fg=COLORS["text"],
                font=("Arial", 11, "bold"),
                relief="raised",
            )
            btn.grid(row=r, column=c, padx=1, pady=1)
            btn.bind("<Button-1>", lambda e, row=r, col=c: on_left_click(row, col))
            btn.bind("<Button-3>", lambda e, row=r, col=c: on_right_click(row, col))
            btn.bind("<Control-Button-1>", lambda e, row=r, col=c: on_right_click(row, col))
            row_buttons.append(btn)
        cells.append(row_cells)
        buttons.append(row_buttons)

    adjust_window_size()


def adjust_window_size():
    cell_px = 26
    width = COLS * cell_px + 40
    height = ROWS * cell_px + 120
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width = min(width, screen_width - 40)
    height = min(height, screen_height - 80)
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    root.geometry(f"{width}x{height}+{x}+{y}")


def place_mines(exclude_row, exclude_col):
    positions = [(r, c) for r in range(ROWS) for c in range(COLS)]
    safe_zone = set()
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            nr = exclude_row + dr
            nc = exclude_col + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS:
                safe_zone.add((nr, nc))
    available = [pos for pos in positions if pos not in safe_zone]
    mine_positions = random.sample(available, MINES)
    for (r, c) in mine_positions:
        cells[r][c]["is_mine"] = True

    for r in range(ROWS):
        for c in range(COLS):
            if cells[r][c]["is_mine"]:
                continue
            count = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr = r + dr
                    nc = c + dc
                    if 0 <= nr < ROWS and 0 <= nc < COLS:
                        if cells[nr][nc]["is_mine"]:
                            count += 1
            cells[r][c]["neighbor_mines"] = count


def on_left_click(row, col):
    global first_click, start_time, timer_running
    if game_over:
        return
    cell = cells[row][col]
    if cell["is_flagged"]:
        return
    if first_click:
        place_mines(row, col)
        first_click = False
        start_time = time.time()
        timer_running = True
        update_timer()
    reveal_cell(row, col)
    check_win()


def on_right_click(row, col):
    global mines_left
    if game_over or first_click:
        return
    cell = cells[row][col]
    btn = buttons[row][col]
    if cell["is_revealed"]:
        return
    if cell["is_flagged"]:
        cell["is_flagged"] = False
        btn.config(text="", bg=COLORS["cell_hidden"])
        mines_left += 1
    else:
        cell["is_flagged"] = True
        btn.config(text="⚑", bg=COLORS["cell_flag"])
        mines_left -= 1
    status_label.config(text=f"Mines: {mines_left}")


def reveal_cell(row, col):
    global game_over
    cell = cells[row][col]
    btn = buttons[row][col]
    if cell["is_revealed"] or cell["is_flagged"]:
        return
    cell["is_revealed"] = True
    btn.config(relief="sunken", bg=COLORS["cell_revealed"])
    if cell["is_mine"]:
        btn.config(text="💣", bg=COLORS["cell_mine"])
        game_over = True
        show_all_mines()
        end_game(False)
        return
    n = cell["neighbor_mines"]
    if n > 0:
        color = NUMBER_COLORS.get(n, COLORS["text"])
        btn.config(text=str(n), fg=color)
    else:
        btn.config(text="")
        flood_fill(row, col)


def flood_fill(row, col):
    stack = [(row, col)]
    while stack:
        r, c = stack.pop()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr = r + dr
                nc = c + dc
                if dr == 0 and dc == 0:
                    continue
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    cell = cells[nr][nc]
                    btn = buttons[nr][nc]
                    if not cell["is_revealed"] and not cell["is_flagged"] and not cell["is_mine"]:
                        cell["is_revealed"] = True
                        btn.config(relief="sunken", bg=COLORS["cell_revealed"])
                        n = cell["neighbor_mines"]
                        if n > 0:
                            color = NUMBER_COLORS.get(n, COLORS["text"])
                            btn.config(text=str(n), fg=color)
                        else:
                            btn.config(text="")
                            stack.append((nr, nc))


def show_all_mines():
    for r in range(ROWS):
        for c in range(COLS):
            cell = cells[r][c]
            btn = buttons[r][c]
            if cell["is_mine"]:
                btn.config(text="💣", bg=COLORS["cell_mine"])
            btn.config(state="disabled")


def check_win():
    global game_over
    if game_over:
        return
    for r in range(ROWS):
        for c in range(COLS):
            cell = cells[r][c]
            if not cell["is_mine"] and not cell["is_revealed"]:
                return
    game_over = True
    for r in range(ROWS):
        for c in range(COLS):
            buttons[r][c].config(state="disabled")
    end_game(True)


def end_game(won):
    global timer_running, best_time
    timer_running = False
    elapsed = int(time.time() - start_time) if start_time is not None else 0

    if won:
        # actualizează best_time local
        if best_time is None or elapsed < best_time:
            best_time = elapsed
        timer_label.config(text=f"Time: {elapsed}    Best: {format_time(best_time)}")

        # scor pentru leaderboard (timp mai mic => scor mai mare)
        if PLAYER_NAME and elapsed > 0:
            raw = 10000 - elapsed * 50
            score_value = max(1, raw)
            lb.add_score(
                "minesweeper",
                PLAYER_NAME,
                score_value,
                extra={
                    "difficulty": difficulty,
                    "time_s": elapsed,
                    "mines": MINES,
                },
            )

        messagebox.showinfo(
            "You win!",
            f"Congratulations, you cleared the board!\nTime: {elapsed}s",
        )
    else:
        messagebox.showinfo("Game Over", "You hit a mine!")


def reset_game():
    set_difficulty()
    create_board()


def update_timer():
    if not timer_running or game_over or start_time is None:
        return
    elapsed = int(time.time() - start_time)
    timer_label.config(text=f"Time: {elapsed}    Best: {format_time(best_time)}")
    root.after(500, update_timer)


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


top_frame = tk.Frame(root, bg=COLORS["status_bg"])
top_frame.pack(pady=(8, 4), fill="x")

status_label = tk.Label(
    top_frame,
    text="Mines: 0",
    font=("Arial", 12, "bold"),
    bg=COLORS["status_bg"],
    fg=COLORS["status_text"],
)
status_label.pack(side="left", padx=10)

timer_label = tk.Label(
    top_frame,
    text="Time: 0    Best: —",
    font=("Arial", 12, "bold"),
    bg=COLORS["status_bg"],
    fg=COLORS["status_text"],
)
timer_label.pack(side="right", padx=10)

reset_button = tk.Button(
    root,
    text="New Game",
    font=("Arial", 12, "bold"),
    bg=COLORS["reset_bg"],
    fg=COLORS["reset_fg"],
    activebackground=COLORS["reset_bg"],
    activeforeground=COLORS["reset_fg"],
    relief="flat",
    padx=20,
    pady=5,
    command=reset_game,
)
reset_button.pack(pady=(0, 8))

board_frame = tk.Frame(root, bg=COLORS["board_bg"], padx=4, pady=4)
board_frame.pack(pady=(0, 10))

ask_player_name()
set_difficulty()
create_board()

root.mainloop()

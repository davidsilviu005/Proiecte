import tkinter as tk
import random
from tkinter import simpledialog
import leaderboard_core as lb

WIDTH = 400
HEIGHT = 600
GROUND_Y = HEIGHT - 50

GRAVITY = 0.55
FLAP_STRENGTH = -9

BASE_PIPE_GAP = 190
MIN_PIPE_GAP = 130

BASE_PIPE_INTERVAL = 1800
MIN_PIPE_INTERVAL = 1000

BASE_PIPE_SPEED = 3
MAX_PIPE_SPEED = 5

BASE_MIN_PIPE_DISTANCE = 200
MIN_MIN_PIPE_DISTANCE = 140

bird_x = 80
bird_y = HEIGHT // 2
bird_vy = 0

pipes = []
score = 0
best_score = 0
game_over = False
score_saved = False
PLAYER_NAME = "Player"

root = tk.Tk()
root.title("Flappy Bird")
root.configure(bg="#1e1e2f")
root.resizable(False, False)

canvas = tk.Canvas(
    root, width=WIDTH, height=HEIGHT, bg="#222333", highlightthickness=0
)
canvas.pack(padx=10, pady=10)

score_label = tk.Label(
    root,
    text="Score: 0 | Best: 0",
    font=("Arial", 14, "bold"),
    bg="#1e1e2f",
    fg="#f8f8f2",
)
score_label.pack(pady=(0, 10))

bird_item = None


def difficulty_factor():
    return min(score / 10.0, 1.0)


def get_pipe_gap():
    f = difficulty_factor()
    return int(BASE_PIPE_GAP - (BASE_PIPE_GAP - MIN_PIPE_GAP) * f)


def get_pipe_interval():
    f = difficulty_factor()
    return int(BASE_PIPE_INTERVAL - (BASE_PIPE_INTERVAL - MIN_PIPE_INTERVAL) * f)


def get_pipe_speed():
    f = min(score / 15.0, 1.0)
    return BASE_PIPE_SPEED + (MAX_PIPE_SPEED - BASE_PIPE_SPEED) * f


def get_min_pipe_distance():
    f = difficulty_factor()
    return int(BASE_MIN_PIPE_DISTANCE - (BASE_MIN_PIPE_DISTANCE - MIN_MIN_PIPE_DISTANCE) * f)


def draw_ground():
    canvas.create_rectangle(0, GROUND_Y, WIDTH, HEIGHT, fill="#444444", outline="")


def draw_bird():
    global bird_item
    r = 14
    if bird_item is not None:
        canvas.delete(bird_item)
    bird_item = canvas.create_oval(
        bird_x - r, bird_y - r, bird_x + r, bird_y + r, fill="#ffeb3b", outline=""
    )


def reset_game():
    global bird_y, bird_vy, pipes, score, game_over, score_saved
    bird_y = HEIGHT // 2
    bird_vy = 0
    pipes = []
    score = 0
    game_over = False
    score_saved = False
    update_score_label()
    canvas.delete("all")
    draw_ground()
    draw_bird()
    root.after(20, game_loop)
    root.after(get_pipe_interval(), spawn_pipe)


def spawn_pipe():
    if game_over:
        return
    if pipes:
        last_x = pipes[-1]["x"]
        distance = WIDTH - last_x
        if distance < get_min_pipe_distance():
            root.after(200, spawn_pipe)
            return
    gap = get_pipe_gap()
    gap_y = random.randint(100, HEIGHT - 150 - gap)
    pipes.append({"x": WIDTH, "gap_y": gap_y, "gap": gap, "passed": False})
    root.after(get_pipe_interval(), spawn_pipe)


def bird_collides_with_rect(rect):
    x1, y1, x2, y2 = rect
    r = 14
    bx1 = bird_x - r
    by1 = bird_y - r
    bx2 = bird_x + r
    by2 = bird_y + r
    return not (bx2 < x1 or bx1 > x2 or by2 < y1 or by1 > y2)


def update_pipes():
    global score, best_score, game_over
    new_pipes = []
    speed = get_pipe_speed()

    for p in pipes:
        p["x"] -= speed
        x = p["x"]
        gap_y = p["gap_y"]
        gap = p["gap"]

        top_rect = (x, 0, x + 70, gap_y)
        bottom_rect = (x, gap_y + gap, x + 70, GROUND_Y)

        if bird_collides_with_rect(top_rect) or bird_collides_with_rect(bottom_rect):
            game_over = True

        if x + 70 < bird_x and not p["passed"]:
            p["passed"] = True
            score += 1
            if score > best_score:
                best_score = score
            update_score_label()

        if x + 70 > 0:
            new_pipes.append(p)

    return new_pipes


def update_score_label():
    score_label.config(text=f"Score: {score} | Best: {best_score}")


def save_score_if_needed():
    global score_saved
    if score_saved:
        return
    score_saved = True
    if PLAYER_NAME and score > 0:
        lb.add_score(
            "flappy_bird",
            PLAYER_NAME,
            score,
            extra={"best_session": best_score},
        )


def game_loop():
    global bird_y, bird_vy, game_over, pipes

    if game_over:
        save_score_if_needed()
        canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2,
            text="Game Over",
            fill="white",
            font=("Arial", 24, "bold"),
        )
        canvas.create_text(
            WIDTH // 2,
            HEIGHT // 2 + 40,
            text="Press Space to restart",
            fill="white",
            font=("Arial", 12),
        )
        return

    bird_vy += GRAVITY
    bird_y += bird_vy

    if bird_y < 0:
        bird_y = 0
        bird_vy = 0
    if bird_y + 14 > GROUND_Y:
        bird_y = GROUND_Y - 14
        game_over = True

    pipes[:] = update_pipes()

    canvas.delete("all")
    draw_ground()
    for p in pipes:
        x = p["x"]
        gap_y = p["gap_y"]
        gap = p["gap"]
        canvas.create_rectangle(x, 0, x + 70, gap_y, fill="#4caf50", outline="")
        canvas.create_rectangle(
            x, gap_y + gap, x + 70, GROUND_Y, fill="#4caf50", outline=""
        )
    draw_bird()

    root.after(20, game_loop)


def flap(event=None):
    global bird_vy, game_over
    if game_over:
        reset_game()
    else:
        bird_vy = FLAP_STRENGTH


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


root.bind("<space>", flap)
root.bind("<Button-1>", flap)

ask_player_name()
reset_game()

sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
ww, wh = WIDTH + 40, HEIGHT + 80
x = int(sw / 2 - ww / 2)
y = int(sh / 2 - wh / 2)
root.geometry(f"{ww}x{wh}+{x}+{y}")

root.mainloop()

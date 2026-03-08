import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
from collections import deque
import leaderboard_core as lb

GRID_SIZE = 20
GRID_WIDTH = 25
GRID_HEIGHT = 25

BASE_SPEED = 140   # ms (la început)
MIN_SPEED = 60     # ms (limită minimă – foarte rapid)
SPEED_ACCEL_PER_SEC = 1.0  # scade cu 1 ms pe secundă

COLORS = {
    "bg": "#1e1e2f",
    "board_bg": "#11111b",
    "snake_head": "#ff6b6b",
    "snake_body": "#f1fa8c",
    "food": "#50fa7b",
    "wall": "#6272a4",
    "hud_text": "#f8f8f2",
}

snake = []
direction = (1, 0)
foods = []
walls = []
game_over = False
score = 0
high_score = 0
start_time = 0.0
PLAYER_NAME = "Player"


root = tk.Tk()
root.title("Snake")
root.configure(bg=COLORS["bg"])

canvas = tk.Canvas(
    root,
    width=GRID_SIZE * GRID_WIDTH,
    height=GRID_SIZE * GRID_HEIGHT,
    bg=COLORS["board_bg"],
    highlightthickness=0,
)
canvas.pack(padx=10, pady=(10, 5))

hud_label = tk.Label(
    root,
    text="Score: 0   High: 0   Time: 00:00",
    font=("Arial", 14, "bold"),
    bg=COLORS["bg"],
    fg=COLORS["hud_text"],
)
hud_label.pack(pady=(0, 10))


def format_time(seconds):
    seconds = int(seconds)
    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"


def get_current_speed():
    elapsed = max(0.0, time.time() - start_time)
    speed = BASE_SPEED - int(SPEED_ACCEL_PER_SEC * elapsed)
    if speed < MIN_SPEED:
        speed = MIN_SPEED
    return speed


def update_hud():
    elapsed = time.time() - start_time
    hud_label.config(
        text=f"Score: {score}   High: {high_score}   Time: {format_time(elapsed)}"
    )
    if not game_over:
        root.after(250, update_hud)


def draw_cell_rect(x, y, color):
    x1 = x * GRID_SIZE
    y1 = y * GRID_SIZE
    x2 = x1 + GRID_SIZE
    y2 = y1 + GRID_SIZE
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=COLORS["board_bg"])


def draw_snake_segment(x, y, is_head=False):
    color = COLORS["snake_head"] if is_head else COLORS["snake_body"]
    draw_cell_rect(x, y, color)


def draw_food(x, y):
    padding = GRID_SIZE * 0.20
    x1 = x * GRID_SIZE + padding
    y1 = y * GRID_SIZE + padding
    x2 = (x + 1) * GRID_SIZE - padding
    y2 = (y + 1) * GRID_SIZE - padding
    canvas.create_oval(x1, y1, x2, y2, fill=COLORS["food"], outline="")


def draw_wall(x, y):
    draw_cell_rect(x, y, COLORS["wall"])


def draw():
    canvas.delete("all")
    for wx, wy in walls:
        draw_wall(wx, wy)
    for fx, fy in foods:
        draw_food(fx, fy)
    if snake:
        head = snake[0]
        draw_snake_segment(head[0], head[1], is_head=True)
        for x, y in snake[1:]:
            draw_snake_segment(x, y, is_head=False)


def generate_walls():
    global walls
    walls = []
    num_walls = 40
    forbidden = set(snake)
    center_x = GRID_WIDTH // 2
    center_y = GRID_HEIGHT // 2

    for _ in range(num_walls * 5):
        if len(walls) >= num_walls:
            break
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) in forbidden:
            continue
        if abs(x - center_x) <= 2 and abs(y - center_y) <= 2:
            continue
        if (x, y) in walls:
            continue
        walls.append((x, y))


def get_reachable_empty_cells():
    blocked = set(walls) | set(snake)
    head = snake[0]
    if head in walls:
        return []
    visited = set()
    q = deque()
    q.append(head)
    visited.add(head)

    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT):
                continue
            if (nx, ny) in visited:
                continue
            if (nx, ny) in blocked and (nx, ny) != head:
                continue
            visited.add((nx, ny))
            q.append((nx, ny))

    empty = [cell for cell in visited if cell not in set(snake) and cell not in set(walls)]
    return empty


def spawn_initial_foods():
    global foods
    foods = []
    reachable = get_reachable_empty_cells()
    random.shuffle(reachable)
    desired = random.randint(5, 8)
    count = min(desired, len(reachable))
    foods = reachable[:count]


def spawn_single_food():
    global foods
    reachable = get_reachable_empty_cells()
    used = set(foods)
    candidates = [cell for cell in reachable if cell not in used]
    if not candidates:
        return
    foods.append(random.choice(candidates))


def reset_game():
    global snake, direction, foods, walls, game_over, score, start_time
    snake = [
        (GRID_WIDTH // 2, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
        (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2),
    ]
    direction = (1, 0)
    game_over = False
    score = 0
    start_time = time.time()
    generate_walls()
    spawn_initial_foods()
    draw()
    update_hud()


def change_direction(new_dx, new_dy):
    global direction
    dx, dy = direction
    if (dx, dy) == (-new_dx, -new_dy):
        return
    direction = (new_dx, new_dy)


def step():
    global game_over, score, high_score

    if game_over:
        return

    dx, dy = direction
    head_x, head_y = snake[0]
    new_head = (head_x + dx, head_y + dy)

    if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
        end_game()
        return

    if new_head in snake:
        end_game()
        return

    if new_head in walls:
        end_game()
        return

    snake.insert(0, new_head)

    if new_head in foods:
        score += 1
        if score > high_score:
            high_score = score
        foods.remove(new_head)
        spawn_single_food()
    else:
        snake.pop()

    draw()
    root.after(get_current_speed(), step)


def end_game():
    global game_over
    game_over = True
    elapsed = time.time() - start_time

    # Save to leaderboard
    if PLAYER_NAME and score > 0:
        lb.add_score(
            "snake",
            PLAYER_NAME,
            score,
            extra={
                "time_s": int(elapsed),
                "session_high": high_score,
            },
        )

    messagebox.showinfo(
        "Game Over",
        f"You died!\nScore: {score}\nHighscore: {high_score}\nTime: {format_time(elapsed)}",
    )
    reset_game()
    root.after(get_current_speed(), step)


def on_key_press(event):
    key = event.keysym
    if key in ("Up", "w", "W"):
        change_direction(0, -1)
    elif key in ("Down", "s", "S"):
        change_direction(0, 1)
    elif key in ("Left", "a", "A"):
        change_direction(-1, 0)
    elif key in ("Right", "d", "D"):
        change_direction(1, 0)


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


root.bind("<KeyPress>", on_key_press)

window_width = GRID_SIZE * GRID_WIDTH + 20
window_height = GRID_SIZE * GRID_HEIGHT + 70
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coord = int((screen_width / 2) - (window_width / 2))
y_coord = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")

ask_player_name()
reset_game()
root.after(get_current_speed(), step)
root.mainloop()

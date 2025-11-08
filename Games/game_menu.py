import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

PYTHON = sys.executable
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def run_game(filename):
    path = os.path.join(BASE_DIR, filename)
    if not os.path.exists(path):
        messagebox.showerror("Error", f"Game file not found:\n{filename}")
        return
    subprocess.Popen([PYTHON, path])


def play_tictactoe():
    run_game("tic_tac_toe.py")


def play_snake():
    run_game("snake.py")


def play_minesweeper():
    run_game("minesweeper.py")


def play_2048():
    run_game("game_2048.py")


def play_flappy():
    run_game("flappy_bird.py")


def play_memory():
    run_game("memory_match.py")


def show_leaderboards():
    # deschide fereastra cu leaderboard-uri
    run_game("leaderboard_menu.py")


root = tk.Tk()
root.title("Game Menu")
root.configure(bg="#1E1E2F")

title_label = tk.Label(
    root,
    text="Choose a game",
    font=("Arial", 18, "bold"),
    bg="#1E1E2F",
    fg="#F8F8F2",
)
title_label.pack(pady=20, padx=20)

btn_style = {
    "font": ("Arial", 14, "bold"),
    "width": 22,
    "height": 1,
    "bd": 0,
    "relief": "flat",
    "bg": "#50FA7B",
    "fg": "#1E1E2F",
    "activebackground": "#8BE9FD",
    "activeforeground": "#1E1E2F",
}

tk.Button(root, text="Tic Tac Toe", command=play_tictactoe, **btn_style).pack(pady=4)
tk.Button(root, text="Snake", command=play_snake, **btn_style).pack(pady=4)
tk.Button(root, text="Minesweeper", command=play_minesweeper, **btn_style).pack(pady=4)
tk.Button(root, text="2048 (5x5)", command=play_2048, **btn_style).pack(pady=4)
tk.Button(root, text="Flappy Bird", command=play_flappy, **btn_style).pack(pady=4)
tk.Button(root, text="Memory Match", command=play_memory, **btn_style).pack(pady=4)

# buton pentru leaderboard
tk.Button(
    root,
    text="Leaderboards",
    command=show_leaderboards,
    font=("Arial", 12, "bold"),
    width=22,
    bd=0,
    relief="flat",
    bg="#6272A4",
    fg="#F8F8F2",
    activebackground="#8BE9FD",
    activeforeground="#1E1E2F",
).pack(pady=(10, 4))

tk.Button(
    root,
    text="Exit",
    command=root.destroy,
    font=("Arial", 12, "bold"),
    width=10,
    bd=0,
    relief="flat",
    bg="#FF5555",
    fg="#1E1E2F",
    activebackground="#FF79C6",
    activeforeground="#1E1E2F",
).pack(pady=12)

window_width = 360
window_height = 520  # puțin mai înalt pentru butonul nou
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

root.mainloop()

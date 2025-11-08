import tkinter as tk
from tkinter import ttk, messagebox
import leaderboard_core as lb

root = tk.Tk()
root.title("Leaderboards")
root.configure(bg="#1e1e2f")

title_label = tk.Label(
    root,
    text="Leaderboards",
    font=("Arial", 18, "bold"),
    bg="#1e1e2f",
    fg="#f8f8f2",
)
title_label.pack(pady=(10, 5), padx=10)

# Dropdown for games
games_frame = tk.Frame(root, bg="#1e1e2f")
games_frame.pack(pady=(5, 5), padx=10, fill="x")

tk.Label(
    games_frame,
    text="Select game:",
    font=("Arial", 12),
    bg="#1e1e2f",
    fg="#f8f8f2",
).pack(side="left", padx=(0, 8))

game_var = tk.StringVar()
game_combo = ttk.Combobox(
    games_frame,
    textvariable=game_var,
    state="readonly",
    width=25,
)
game_combo.pack(side="left", padx=(0, 8))

def refresh_game_list():
    games = lb.get_all_games()
    if not games:
        games = ["(no scores yet)"]
    game_combo["values"] = games
    if games:
        game_var.set(games[0])

refresh_game_list()

# Frame for leaderboard list
list_frame = tk.Frame(root, bg="#1e1e2f")
list_frame.pack(padx=10, pady=(5, 10), fill="both", expand=True)

listbox = tk.Listbox(
    list_frame,
    font=("Consolas", 11),
    bg="#25253a",
    fg="#f8f8f2",
    width=60,
    height=12,
    selectbackground="#44475a",
    borderwidth=0,
    highlightthickness=0,
)
listbox.pack(side="left", fill="both", expand=True)

scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

def show_leaderboard():
    game = game_var.get()
    if not game or game == "(no scores yet)":
        messagebox.showinfo("No scores", "No scores available yet.")
        return

    entries = lb.get_leaderboard(game, limit=20)
    listbox.delete(0, tk.END)

    if not entries:
        listbox.insert(tk.END, "No scores for this game yet.")
        return

    for i, e in enumerate(entries, start=1):
        extra_str = ""
        if e.get("extra"):
            parts = []
            for k, v in e["extra"].items():
                parts.append(f"{k}={v}")
                if len(parts) >= 2:
                    break
            if parts:
                extra_str = " | " + ", ".join(parts)

        line = f"{i:2}. {e['player']:<12}  score={e['score']:<6}  {e['time']}{extra_str}"
        listbox.insert(tk.END, line)

btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack(pady=(0, 10))

btn_refresh = tk.Button(
    btn_frame,
    text="Refresh Games",
    font=("Arial", 10, "bold"),
    bg="#6272a4",
    fg="#f8f8f2",
    bd=0,
    padx=10,
    pady=4,
    command=refresh_game_list,
)
btn_refresh.pack(side="left", padx=5)

btn_show = tk.Button(
    btn_frame,
    text="Show Leaderboard",
    font=("Arial", 10, "bold"),
    bg="#50fa7b",
    fg="#1e1e2f",
    bd=0,
    padx=10,
    pady=4,
    command=show_leaderboard,
)
btn_show.pack(side="left", padx=5)

btn_close = tk.Button(
    btn_frame,
    text="Close",
    font=("Arial", 10, "bold"),
    bg="#ff5555",
    fg="#1e1e2f",
    bd=0,
    padx=10,
    pady=4,
    command=root.destroy,
)
btn_close.pack(side="left", padx=5)

# Center window
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
ww, wh = 700, 400
x = int(sw / 2 - ww / 2)
y = int(sh / 2 - wh / 2)
root.geometry(f"{ww}x{wh}+{x}+{y}")

root.mainloop()

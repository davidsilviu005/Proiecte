import tkinter as tk
import random
import time
from tkinter import simpledialog
import leaderboard_core as lb

# Sentences to type
TEXTS = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a great language for learning to code.",
    "Typing fast and accurately takes practice and focus.",
    "Games are a fun way to improve programming skills.",
    "Never stop learning because life never stops teaching.",
    "Smooth code and clean design make projects enjoyable.",
    "Writing your own games is a powerful way to learn.",
    "Practice every day and you will see real progress.",
]

current_text = ""
start_time = None
end_time = None
timer_running = False

PLAYER_NAME = "Player"
score_saved = False

# ---------- Timer logic ----------

def start_timer():
    global start_time, timer_running
    start_time = time.time()
    timer_running = True
    update_timer_label()

def stop_timer():
    global end_time, timer_running
    if timer_running:
        end_time = time.time()
        timer_running = False

def update_timer_label():
    if not timer_running or start_time is None:
        return
    elapsed = time.time() - start_time
    timer_label.config(text=f"Time: {elapsed:.1f} s")
    root.after(100, update_timer_label)

# ---------- Test logic ----------

def new_test():
    global current_text, start_time, end_time, timer_running, score_saved
    current_text = random.choice(TEXTS)
    text_label.config(text=current_text)

    typing_area.config(state="normal")
    typing_area.delete("1.0", tk.END)
    typing_area.focus_set()

    result_label.config(text="Start typing, then press Finish.", fg="#f8f8f2")
    wpm_label.config(text="WPM: -")
    acc_label.config(text="Accuracy: -")
    timer_label.config(text="Time: 0.0 s")

    start_time = None
    end_time = None
    timer_running = False
    score_saved = False

def on_typing(event):
    global start_time, timer_running
    if start_time is None and not timer_running:
        # start timing on first key press
        start_timer()

def finish_test():
    global start_time, end_time, timer_running, score_saved
    if start_time is None:
        result_label.config(text="You haven't started typing yet.", fg="#ffb86c")
        return

    stop_timer()
    if end_time is None:
        end_time = time.time()

    typed = typing_area.get("1.0", tk.END).rstrip("\n")
    target = current_text

    elapsed = end_time - start_time
    if elapsed <= 0:
        elapsed = 0.001

    # Calculate WPM (standard: 5 chars = 1 word)
    num_chars = len(typed)
    wpm = (num_chars / 5) / (elapsed / 60)

    # Accuracy: character-wise
    correct_chars = 0
    for i in range(min(len(typed), len(target))):
        if typed[i] == target[i]:
            correct_chars += 1
    max_len = max(len(typed), len(target)) or 1
    accuracy = (correct_chars / max_len) * 100

    timer_label.config(text=f"Time: {elapsed:.1f} s")
    wpm_label.config(text=f"WPM: {wpm:.1f}")
    acc_label.config(text=f"Accuracy: {accuracy:.1f}%")

    result_label.config(
        text="Test finished! Press New Test to try again.",
        fg="#50fa7b",
    )

    # --- save to leaderboard once per test ---
    if not score_saved and PLAYER_NAME:
        score_value = max(1, int(wpm * (accuracy / 100.0)))
        lb.add_score(
            "typing_test",
            PLAYER_NAME,
            score_value,
            extra={
                "wpm": round(wpm, 1),
                "accuracy": round(accuracy, 1),
                "time_s": round(elapsed, 1),
            },
        )
        score_saved = True

# ---------- UI Setup ----------

root = tk.Tk()
root.title("Typing Speed Test")
root.configure(bg="#1e1e2f")

title_label = tk.Label(
    root,
    text="Typing Speed Test",
    font=("Arial", 18, "bold"),
    bg="#1e1e2f",
    fg="#f8f8f2",
)
title_label.pack(pady=(10, 5))

text_frame = tk.Frame(root, bg="#1e1e2f")
text_frame.pack(pady=(5, 5), padx=10, fill="x")

instruction_label = tk.Label(
    text_frame,
    text="Type the text below as fast and accurately as you can:",
    font=("Arial", 12),
    bg="#1e1e2f",
    fg="#f8f8f2",
    anchor="w",
)
instruction_label.pack(fill="x")

text_label = tk.Label(
    text_frame,
    text="",
    font=("Arial", 12, "italic"),
    bg="#25253a",
    fg="#f8f8f2",
    wraplength=500,
    justify="left",
    padx=10,
    pady=10,
)
text_label.pack(fill="x", pady=(5, 5))

typing_area = tk.Text(
    root,
    height=5,
    width=60,
    font=("Consolas", 12),
    bg="#30304a",
    fg="#f8f8f2",
    insertbackground="#f8f8f2",
    wrap="word",
    relief="flat",
)
typing_area.pack(padx=10, pady=(5, 5))

typing_area.bind("<Key>", on_typing)

stats_frame = tk.Frame(root, bg="#1e1e2f")
stats_frame.pack(pady=(5, 5))

timer_label = tk.Label(
    stats_frame,
    text="Time: 0.0 s",
    font=("Arial", 12, "bold"),
    bg="#1e1e2f",
    fg="#f8f8f2",
)
timer_label.grid(row=0, column=0, padx=10)

wpm_label = tk.Label(
    stats_frame,
    text="WPM: -",
    font=("Arial", 12, "bold"),
    bg="#1e1e2f",
    fg="#f8f8f2",
)
wpm_label.grid(row=0, column=1, padx=10)

acc_label = tk.Label(
    stats_frame,
    text="Accuracy: -",
    font=("Arial", 12, "bold"),
    bg="#1e1e2f",
    fg="#f8f8f2",
)
acc_label.grid(row=0, column=2, padx=10)

result_label = tk.Label(
    root,
    text="Press New Test to start.",
    font=("Arial", 12),
    bg="#1e1e2f",
    fg="#f8f8f2",
)
result_label.pack(pady=(5, 5))

buttons_frame = tk.Frame(root, bg="#1e1e2f")
buttons_frame.pack(pady=(5, 10))

btn_new = tk.Button(
    buttons_frame,
    text="New Test",
    font=("Arial", 12, "bold"),
    bg="#8bc34a",
    fg="#1e1e2f",
    bd=0,
    padx=20,
    pady=5,
    command=new_test,
)
btn_new.pack(side="left", padx=10)

btn_finish = tk.Button(
    buttons_frame,
    text="Finish",
    font=("Arial", 12, "bold"),
    bg="#ffb86c",
    fg="#1e1e2f",
    bd=0,
    padx=20,
    pady=5,
    command=finish_test,
)
btn_finish.pack(side="left", padx=10)

def finish_on_enter(event):
    finish_test()

root.bind("<Return>", finish_on_enter)

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
new_test()

# Center window
sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()
ww, wh = 640, 420
x = int(sw / 2 - ww / 2)
y = int(sh / 2 - ww / 2)
root.geometry(f"{ww}x{wh}+{x}+{y}")

root.mainloop()

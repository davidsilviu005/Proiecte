# app.py

import tkinter as tk
from tkinter import ttk

from db.database import init_db, get_connection
from ui.tasks_view import TasksView
from ui.notes_view import NotesView


class SmartStudyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Smart Study Assistant")
        self.geometry("1000x650")

        # One reusable DB connection for the whole app
        self.conn = get_connection()

        self._create_widgets()

    def _create_widgets(self):
        # Notebook = tab control
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # -------- Tasks tab --------
        tasks_frame = ttk.Frame(notebook)
        notebook.add(tasks_frame, text="Tasks")
        self.tasks_view = TasksView(tasks_frame, self.conn)

        # -------- Notes tab (with AI) --------
        notes_frame = ttk.Frame(notebook)
        notebook.add(notes_frame, text="Notes")
        self.notes_view = NotesView(notes_frame, self.conn)

        # Later you can add:
        # - Dashboard tab
        # - Courses tab

    def on_close(self):
        # Close DB connection and exit
        if self.conn:
            self.conn.close()
        self.destroy()


if __name__ == "__main__":
    # Ensure database and tables exist
    init_db()

    # Start the GUI app
    app = SmartStudyApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()

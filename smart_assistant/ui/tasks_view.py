# ui/tasks_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date


class TasksView:
    def __init__(self, parent, conn):
        self.parent = parent
        self.conn = conn

        self.selected_task_id = None

        self._build_ui()
        self.load_tasks()

    def _build_ui(self):
        # ---------- Form frame ----------
        form_frame = ttk.LabelFrame(self.parent, text="Add / Edit Task")
        form_frame.pack(fill="x", padx=10, pady=10)

        # Title
        ttk.Label(form_frame, text="Title:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.title_entry = ttk.Entry(form_frame, width=40)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Due date
        ttk.Label(form_frame, text="Due date (YYYY-MM-DD):").grid(
            row=1, column=0, sticky="w", padx=5, pady=5
        )
        self.due_entry = ttk.Entry(form_frame, width=20)
        self.due_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Description (optional)
        ttk.Label(form_frame, text="Description:").grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        self.desc_text = tk.Text(form_frame, width=40, height=4)
        self.desc_text.grid(row=2, column=1, padx=5, pady=5)

        # Buttons: Save, Clear
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=0, column=2, rowspan=3, padx=10, pady=5, sticky="n")

        save_btn = ttk.Button(buttons_frame, text="Save task", command=self.add_task)
        save_btn.pack(fill="x", pady=2)

        clear_btn = ttk.Button(buttons_frame, text="Clear form", command=self.clear_form)
        clear_btn.pack(fill="x", pady=2)

        # ---------- Task list ----------
        list_frame = ttk.Frame(self.parent)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "title", "due_date", "status")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.heading("due_date", text="Due date")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("title", width=300)
        self.tree.column("due_date", width=100, anchor="center")
        self.tree.column("status", width=80, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bind selection
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # ---------- Actions under list ----------
        actions_frame = ttk.Frame(self.parent)
        actions_frame.pack(fill="x", padx=10, pady=5)

        done_btn = ttk.Button(actions_frame, text="Mark as done", command=self.mark_done)
        done_btn.pack(side="left", padx=5)

        delete_btn = ttk.Button(actions_frame, text="Delete task", command=self.delete_task)
        delete_btn.pack(side="left", padx=5)

        refresh_btn = ttk.Button(actions_frame, text="Refresh", command=self.load_tasks)
        refresh_btn.pack(side="right", padx=5)

    # ---------- DB interaction ----------

    def load_tasks(self):
        """Load tasks from DB into the table."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        cur = self.conn.cursor()
        cur.execute("SELECT id, title, due_date, status FROM tasks ORDER BY due_date;")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)

        self.selected_task_id = None

    def add_task(self):
        """Insert a new task in the DB."""
        title = self.title_entry.get().strip()
        due_date = self.due_entry.get().strip() or date.today().isoformat()
        description = self.desc_text.get("1.0", tk.END).strip()

        if not title:
            messagebox.showerror("Error", "Title is required.")
            return

        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO tasks (title, due_date, description, status) VALUES (?, ?, ?, 'pending');",
            (title, due_date, description),
        )
        self.conn.commit()

        self.clear_form()
        self.load_tasks()

    def delete_task(self):
        """Delete the selected task."""
        if not self.selected_task_id:
            messagebox.showwarning("No selection", "Please select a task first.")
            return

        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            return

        cur = self.conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = ?;", (self.selected_task_id,))
        self.conn.commit()

        self.load_tasks()

    def mark_done(self):
        """Mark the selected task as done."""
        if not self.selected_task_id:
            messagebox.showwarning("No selection", "Please select a task first.")
            return

        cur = self.conn.cursor()
        cur.execute("UPDATE tasks SET status = 'done' WHERE id = ?;", (self.selected_task_id,))
        self.conn.commit()

        self.load_tasks()

    # ---------- Helpers ----------

    def on_select(self, event):
        """When the user selects a row, store its ID."""
        selected = self.tree.selection()
        if not selected:
            self.selected_task_id = None
            return

        item = self.tree.item(selected[0])
        values = item["values"]
        self.selected_task_id = values[0]

    def clear_form(self):
        """Clear form inputs."""
        self.title_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.selected_task_id = None

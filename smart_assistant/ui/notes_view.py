# ui/notes_view.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ai.summarizer import summarize_text


class NotesView:
    def __init__(self, parent, conn):
        self.parent = parent
        self.conn = conn
        self.selected_note_id = None

        self._build_ui()
        self.load_notes()

    def _build_ui(self):
        # Top: list of notes
        top_frame = ttk.Frame(self.parent)
        top_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "title")
        self.tree = ttk.Treeview(top_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("title", text="Title")
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("title", width=300)
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(top_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Bottom: note text + summary button + summary area
        bottom_frame = ttk.LabelFrame(self.parent, text="Note details")
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Original note
        ttk.Label(bottom_frame, text="Content:").grid(
            row=0, column=0, sticky="nw", padx=5, pady=5
        )
        self.content_text = tk.Text(bottom_frame, width=60, height=10)
        self.content_text.grid(row=0, column=1, padx=5, pady=5)

        # Buttons (summarize, save note, save summary)
        btn_frame = ttk.Frame(bottom_frame)
        btn_frame.grid(row=0, column=2, padx=5, pady=5, sticky="n")

        summarize_btn = ttk.Button(
            btn_frame, text="Summarize with AI", command=self.on_summarize
        )
        summarize_btn.pack(fill="x", pady=2)

        save_note_btn = ttk.Button(btn_frame, text="Save note", command=self.save_note)
        save_note_btn.pack(fill="x", pady=2)

        # NEW BUTTON: Save summary to file
        save_summary_btn = ttk.Button(
            btn_frame, text="Save summary to file", command=self.save_summary_to_file
        )
        save_summary_btn.pack(fill="x", pady=2)

        # Summary display
        ttk.Label(bottom_frame, text="AI Summary:").grid(
            row=1, column=0, sticky="nw", padx=5, pady=5
        )
        self.summary_text = tk.Text(bottom_frame, width=60, height=8, state="disabled")
        self.summary_text.grid(row=1, column=1, padx=5, pady=5)

    # -------- DB operations --------

    def load_notes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        cur = self.conn.cursor()
        cur.execute("SELECT id, title FROM notes ORDER BY id DESC;")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)

        self.selected_note_id = None
        self.content_text.delete("1.0", tk.END)
        self._set_summary("")

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            self.selected_note_id = None
            return

        item = self.tree.item(selected[0])
        note_id, title = item["values"]
        self.selected_note_id = note_id

        # Load content from DB
        cur = self.conn.cursor()
        cur.execute("SELECT content FROM notes WHERE id = ?;", (note_id,))
        row = cur.fetchone()
        content = row[0] if row else ""

        self.content_text.delete("1.0", tk.END)
        self.content_text.insert(tk.END, content)
        self._set_summary("")

    def save_note(self):
        title = "Untitled note"
        content = self.content_text.get("1.0", tk.END).strip()

        if self.selected_note_id:  # update
            cur = self.conn.cursor()
            cur.execute(
                "UPDATE notes SET content = ? WHERE id = ?;",
                (content, self.selected_note_id),
            )
            self.conn.commit()
        else:  # insert new
            if not content:
                messagebox.showwarning("Empty", "Write something before saving.")
                return
            # Derive title from first line
            first_line = content.splitlines()[0] if content else "Untitled note"
            title = first_line[:50]
            cur = self.conn.cursor()
            cur.execute(
                "INSERT INTO notes (title, content) VALUES (?, ?);",
                (title, content),
            )
            self.conn.commit()
            self.selected_note_id = cur.lastrowid

        self.load_notes()

    # -------- AI integration --------

    def on_summarize(self):
        content = self.content_text.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("No content", "There is no note content to summarize.")
            return

        self._set_summary("Summarizing… please wait...")
        self.parent.update_idletasks()  # force UI refresh

        summary = summarize_text(content, max_sentences=3)
        self._set_summary(summary)

    def _set_summary(self, text: str):
        self.summary_text.config(state="normal")
        self.summary_text.delete("1.0", tk.END)
        self.summary_text.insert(tk.END, text)
        self.summary_text.config(state="disabled")

    # -------- NEW: save summary to file --------

    def save_summary_to_file(self):
        """Save the current AI summary into a .txt file chosen by the user."""
        # Get the summary text
        summary = self.summary_text.get("1.0", tk.END).strip()

        if not summary:
            messagebox.showwarning(
                "No summary",
                "There is no summary to save. Generate a summary first."
            )
            return

        # Ask the user where and under what name to save the file
        file_path = filedialog.asksaveasfilename(
            title="Save summary as...",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        # User cancelled
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(summary)

            messagebox.showinfo(
                "Saved",
                f"Summary saved successfully to:\n{file_path}"
            )
        except Exception as e:
            messagebox.showerror(
                "Error saving file",
                f"Could not save the summary:\n{e}"
            )

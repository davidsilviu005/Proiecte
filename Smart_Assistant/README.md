# Smart Study Assistant

A Python desktop application for organizing study tasks and notes. Its Tkinter interface has separate Tasks and Notes tabs, while SQLite stores the data locally.

## Main parts

- `app.py` starts the interface and opens the database.
- `ui/tasks_view.py` adds, lists, completes, and deletes tasks.
- `ui/notes_view.py` manages notes and can save an AI-generated summary to a file.
- `db/database.py` creates the SQLite tables and manages connections.
- `ai/summarizer.py` uses a Hugging Face model to summarize notes. The model is downloaded on first use, then can work offline.
- `ai/task_parser.py` contains a separate natural-language task parser using the OpenAI API; it is not connected to the main interface.

## Run

Run `python app.py` from this folder. Tkinter and SQLite are part of a typical Python installation. For note summarization, install `transformers` and `torch`; the rest of the app can run without them. The optional task parser requires the `openai` package, an `OPENAI_API_KEY`, and compatibility with the API call used in that file.

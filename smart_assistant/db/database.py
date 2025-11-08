# db/database.py
import sqlite3

DB_NAME = "smart_study.db"


def get_connection():
    """Return a new connection to the SQLite database."""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Create tables if they do not already exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Courses table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        professor TEXT,
        semester TEXT
    );
    """)

    # Tasks table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        title TEXT NOT NULL,
        description TEXT,
        due_date TEXT,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY (course_id) REFERENCES courses(id)
    );
    """)

    # Notes table (for later)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        title TEXT,
        content TEXT,
        FOREIGN KEY (course_id) REFERENCES courses(id)
    );
    """)

    conn.commit()
    conn.close()

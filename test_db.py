import sqlite3
from datetime import datetime, timedelta

def init_db():
    pass

def get_cursor(name="test.db"):
    db = sqlite3.connect(name)
    return db, db.cursor()

def close_db():
    db, cur = get_cursor()
    db.close()

def create_tables():
    db, cur = get_cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        period INT NOT NULL,
        last_completed NOT NULL DEFAULT (DATE('now')),
        created_date TEXT NOT NULL DEFAULT (DATE('now')))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS streak (
        habit_id INTEGER PRIMARY KEY,
        longest_streak INTEGER NOT NULL DEFAULT 0,
        current_streak INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (habit_id) REFERENCES habit(id))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS completed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        completed_date TEXT NOT NULL DEFAULT (DATE('now')),
        FOREIGN KEY (habit_id) REFERENCES habit(id))""")

    db.commit()

from datetime import datetime, timedelta

def insert_test_data():
    db, cur = get_cursor()

    # delete everything because test data needs to be relative to the current date
    cur.execute("DELETE FROM completed")
    cur.execute("DELETE FROM streak")
    cur.execute("DELETE FROM habit")
    cur.execute("DELETE FROM sqlite_sequence WHERE name='habit'") # deletes auto incremented ids
    cur.execute("DELETE FROM sqlite_sequence WHERE name='completed'")


    habits = [
        ("Workout", 1, "2025-05-16", "2025-05-05"),
        ("Read", 7, "2025-05-06", "2025-05-05"),
        ("Clean Room", 30, "2025-05-10", "2025-05-05")
    ]
    cur.executemany("INSERT INTO habit (name, period, last_completed, created_date) VALUES (?, ?, ?, ?)", habits)

    cur.execute("SELECT id FROM habit ORDER BY id")
    habit_ids = [row[0] for row in cur.fetchall()]

    streaks = [
        (habit_ids[0], 5, 2),
        (habit_ids[1], 3, 1),
        (habit_ids[2], 1, 1)
    ]
    cur.executemany(
        "INSERT INTO streak (habit_id, longest_streak, current_streak) VALUES (?, ?, ?)",
        streaks
    )

    today = datetime.today()

    completions = []

    for i in range(4):
        completions.append((habit_ids[0], (today - timedelta(days=6 - i)).strftime('%Y-%m-%d')))
    completions.append((habit_ids[0], (today - timedelta(days=1)).strftime('%Y-%m-%d')))
    completions.append((habit_ids[0], today.strftime('%Y-%m-%d')))

    for i in range(4):
        completions.append((habit_ids[1], (today - timedelta(weeks=3 - i)).strftime('%Y-%m-%d')))

    completions.append((habit_ids[2], (today - timedelta(days=15)).strftime('%Y-%m-%d')))

    cur.executemany(
        "INSERT INTO completed (habit_id, completed_date) VALUES (?, ?)",
        completions
    )

    db.commit()
    db.close()

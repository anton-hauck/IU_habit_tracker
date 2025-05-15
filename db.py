import sqlite3
from datetime import date

def init_db():
    pass

def get_cursor(name="main.db"):
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
        period TEXT NOT NULL,
        created_date TEXT NOT NULL)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS streak (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        longest_streak INTEGER NOT NULL,
        current_streak INTEGER NOT NULL,
        FOREIGN KEY (habit_id) REFERENCES habit(id))""")

    cur.execute("""CREATE TABLE IF NOT EXISTS completed (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        completed_date TEXT NOT NULL,
        FOREIGN KEY (habit_id) REFERENCES habit(id))""")

    db.commit()
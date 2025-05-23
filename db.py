import sqlite3
from datetime import datetime, timedelta
import os


class db_manager:
    def __init__(self, db_name: str="main.db", test_environment: bool=False):
        self.db_name = db_name
        self.test_environment = test_environment
        self.db, self.cur = self.get_cursor()
        self.init_db()

    def init_db(self):
        if self.test_environment:
            self.create_test_tables()
        else:
            self.create_tables()

    def get_cursor(self):
        db = sqlite3.connect(self.db_name)
        return db, db.cursor()

    def close_db(self):
        if self.test_environment:
            os.remove("test.db")
            print("-> Test database removed.")
        self.db.close()

    def create_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS habit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            period INT NOT NULL,
            last_completed NOT NULL DEFAULT (DATE('now')),
            created_date TEXT NOT NULL DEFAULT (DATE('now')))""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS streak (
            habit_id INTEGER PRIMARY KEY,
            longest_streak INTEGER NOT NULL DEFAULT 0,
            current_streak INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (habit_id) REFERENCES habit(id))""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS completed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_date TEXT NOT NULL DEFAULT (DATE('now')),
            FOREIGN KEY (habit_id) REFERENCES habit(id))""")

        self.db.commit()
        self.init_predefined_habits()

    def init_predefined_habits(self):
        pass

    def create_test_tables(self):
        self.cur.execute("DROP TABLE IF EXISTS completed")
        self.cur.execute("DROP TABLE IF EXISTS streak")
        self.cur.execute("DROP TABLE IF EXISTS habit")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS habit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            period INT NOT NULL,
            last_completed NOT NULL DEFAULT (DATE('now')),
            created_date TEXT NOT NULL DEFAULT (DATE('now')))""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS streak (
            habit_id INTEGER PRIMARY KEY,
            longest_streak INTEGER NOT NULL DEFAULT 0,
            current_streak INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (habit_id) REFERENCES habit(id))""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS completed (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            completed_date TEXT NOT NULL DEFAULT (DATE('now')),
            FOREIGN KEY (habit_id) REFERENCES habit(id))""")

        today = datetime.today().date()

        habits = [
            (1, "Python programming", 1, -1, -30),
            (2, "Shop groceries", 7, -8, -30),
            (3, "Deepclean House", 30, -7, -30),
            (4, "Sport", 3, -2, -30),
            (5, "Practice piano", 2, -2, -30),
        ]

        self.cur.executemany(
            "INSERT INTO habit (id, name, period, last_completed, created_date) VALUES (?, ?, ?, ?, ?)",
            [
                (id, name, period,
                 (today + timedelta(days=last_completed)).strftime('%Y-%m-%d'),
                 (today + timedelta(days=created)).strftime('%Y-%m-%d'))
                for id, name, period, last_completed, created in habits
            ]
        )

        # Insert completions
        raw_completions = [
            (1, -29), (2, -29), (1, -28), (4, -28), (3, -27), (1, -27), (5, -26), (2, -26),
            (1, -25), (2, -25), (1, -24), (2, -24), (1, -23), (5, -22), (3, -22), (1, -22),
            (1, -21), (1, -20), (4, -19), (2, -18), (4, -18), (1, -18), (1, -17), (2, -17),
            (1, -16), (5, -16), (4, -16), (3, -15), (1, -15), (5, -15), (1, -14), (5, -14),
            (4, -14), (5, -13), (1, -13), (2, -12), (3, -12), (4, -12), (1, -12), (5, -12),
            (2, -11), (4, -11), (1, -11), (5, -11), (2, -11), (5, -10), (1, -10), (1, -10),
            (1, -9), (1, -8), (5, -8), (4, -8), (2, -8), (1, -7), (4, -7), (2, -7), (1, -6),
            (5, -6), (1, -5), (1, -5), (1, -5), (1, -4), (4, -4), (5, -4), (1, -3), (4, -3),
            (1, -3), (1, -2), (4, -2), (1, -1)
        ]

        completions = [
            (habit_id, (today + timedelta(days=offset)).strftime('%Y-%m-%d'))
            for habit_id, offset in raw_completions
        ]
        self.cur.executemany("INSERT INTO completed (habit_id, completed_date) VALUES (?, ?)", completions)

        streaks = [
            (1, 18, 18),
            (2, 4, 4),
            (3, 1, 1),
            (4, 7, 7),
            (5, 7, 0),
        ]

        self.cur.executemany("INSERT INTO streak (habit_id, longest_streak, current_streak) VALUES (?, ?, ?)", streaks)

        self.db.commit()
        self.db.close()

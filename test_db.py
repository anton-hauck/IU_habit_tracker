import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict


def init_db():
    pass

def get_cursor(name="test.db"):
    db = sqlite3.connect(name)
    return db, db.cursor()

def close_db():
    db, cur = get_cursor()
    db.close()

def create_test_tables():
    db, cur = get_cursor()

    cur.execute("DROP TABLE IF EXISTS completed")
    cur.execute("DROP TABLE IF EXISTS streak")
    cur.execute("DROP TABLE IF EXISTS habit")

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

    today = datetime.today().date()

    habits = [
        (1, "Shop groceries", 7, today - timedelta(days=1), today - timedelta(days=29)),
        (2, "Python programming", 1, today - timedelta(days=5), today - timedelta(days=29)),
        (3, "Deepclean House", 30, today - timedelta(days=17), today - timedelta(days=29)),
    ]
    cur.executemany(
        "INSERT INTO habit (id, name, period, last_completed, created_date) VALUES (?, ?, ?, ?, ?)",
        [(id, name, period, last_completed.strftime('%Y-%m-%d'), created.strftime('%Y-%m-%d'))
         for id, name, period, last_completed, created in habits]
    )

    completion_raw = [
        (1, -29), (2, -25), (1, -28), (1, -26), (3, -25), (1, -24), (1, -23), (2, -23),
        (1, -22), (2, -21), (1, -21), (1, -20), (1, -18), (3, -17), (2, -17), (1, -17),
        (1, -16), (1, -15), (1, -14), (1, -13), (2, -12), (1, -11), (1, -10), (1, -9),
        (2, -8), (1, -7), (1, -6), (2, -5), (1, -4), (1, -3), (1, -2), (1, -1)
    ]

    completions = [(habit_id, (today + timedelta(days=offset)).strftime('%Y-%m-%d'))
                   for habit_id, offset in completion_raw]
    cur.executemany("INSERT INTO completed (habit_id, completed_date) VALUES (?, ?)", completions)

    completions_by_habit = defaultdict(list)
    for habit_id, date_str in completions:
        completions_by_habit[habit_id].append(datetime.strptime(date_str, "%Y-%m-%d").date())

    streak_entries = []
    for habit_id, dates in completions_by_habit.items():
        period = next(h[2] for h in habits if h[0] == habit_id)
        dates = sorted(set(dates))

        longest = current = 1
        for i in range(1, len(dates)):
            expected = dates[i - 1] + timedelta(days=period)
            if dates[i] <= expected:
                current += 1
                longest = max(longest, current)
            else:
                current = 1

        last_completion = max(dates)
        if last_completion + timedelta(days=period) >= today:
            streak_entries.append((habit_id, longest, current))
        else:
            streak_entries.append((habit_id, longest, 0))

    cur.executemany("INSERT INTO streak (habit_id, longest_streak, current_streak) VALUES (?, ?, ?)", streak_entries)

    db.commit()
    db.close()
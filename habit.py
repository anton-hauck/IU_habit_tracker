from db import get_cursor

class Habit:
    def __init__(self, id: int, name: str, period: str, open: bool=True):
        self.id = id
        self.name = name
        self.period = period
        self.open = open
        self.db, self.cur = get_cursor()

    def complete(self):
        self.cur.execute("INSERT INTO completed (habit_id) VALUES (?)", (self.id,)) # "self.id," because a tupel is expected
        self.db.commit()

    def broken(self):
        self.cur.execute("UPDATE streak SET current_streak = 0 WHERE habit_id = ?", (self.id,))
        self.db.commit()

    def is_open(self):
        self.cur.execute("SELECT id FROM habit WHERE habit_id = ?", (self.id,))

    def get_current_streak(self):
        self.cur.execute("SELECT current_streak FROM streak WHERE habit_id = ?", (self.id,))
        self.db.commit()
        return self.cur.fetchone()[0]

    def get_longest_streak(self):
        self.cur.execute("SELECT longest_streak FROM streak WHERE habit_id = ?", (self.id,))
        self.db.commit()
        return self.cur.fetchone()[0]


    def __repr__(self):
        return f"Habit {self.id} {self.name} {self.period}"
from db import db_manager
from datetime import datetime, timedelta

class Habit:
    def __init__(self, id: int, name: str, period: int, last_completed: str, db_manager, open: bool=True):
        self.id = id
        self.name = name
        self.period = period
        self.open = open
        self.last_completed = last_completed
        self.db_manager = db_manager
        self.db, self.cur = db_manager.get_cursor()
        self.is_open()

    def complete(self):
        self.cur.execute("INSERT INTO completed (habit_id) VALUES (?)", (self.id,)) # "self.id," because a tupel is expected
        self.cur.execute("UPDATE habit SET last_completed = ? WHERE id = ?", (datetime.today().date(), self.id,))
        self.db.commit()
        if self.open:
            self.cur.execute("UPDATE streak SET current_streak = current_streak + 1 WHERE habit_id = ?", (self.id,))
            self.db.commit()
            self.update_longest_streaks()
            self.open = False


    def broken(self):
        self.cur.execute("UPDATE streak SET current_streak = 0 WHERE habit_id = ?", (self.id,))
        self.db.commit()

    def is_open(self):
        # fetchone gives a tuple, thus [0] returns the date
        created = datetime.strptime(self.cur.execute("SELECT created_date FROM habit WHERE id = ?", (self.id,)).fetchone()[0], "%Y-%m-%d").date()
        last = datetime.strptime(self.cur.execute("SELECT last_completed FROM habit WHERE id = ?", (self.id,)).fetchone()[0], "%Y-%m-%d").date()

        # checks if today and last completed are in the same period cycle.
        # The period cycle is determined by dividing through the period
        days_since_created = (datetime.today().date() - created).days
        current_period_cycle = days_since_created // self.period

        days_since_last_completed = (last - created).days
        last_completed_period_cycle = days_since_last_completed // self.period

        if created == last:
            self.open = True
        else:
            self.open = last_completed_period_cycle < current_period_cycle

        # is today past the last expected deadline for completion
        if last + timedelta(days=self.period) < datetime.today().date():
            self.broken()

    def get_current_streak(self):
        self.cur.execute("SELECT current_streak FROM streak WHERE habit_id = ?", (self.id,))
        self.db.commit()
        return self.cur.fetchone()[0]

    def get_longest_streak(self):
        self.cur.execute("SELECT longest_streak FROM streak WHERE habit_id = ?", (self.id,))
        self.db.commit()
        return self.cur.fetchone()[0]

    def update_longest_streaks(self):
        if self.get_current_streak() > self.get_longest_streak():
            self.cur.execute("UPDATE streak SET longest_streak = ? WHERE habit_id = ?", (self.get_current_streak(), self.id,))
            self.db.commit()


    def __repr__(self):
        return f"{self.id} {self.name} {self.period} {self.last_completed} {self.open}"
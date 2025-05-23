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
        """
        Completes a habit by updating the database and streaks.
        If the habit is open, the current streak is incremented, and the longest streak is updated.
        """
        self.cur.execute("INSERT INTO completed (habit_id) VALUES (?)", (self.id,)) # "self.id," because a tupel is expected
        self.cur.execute("UPDATE habit SET last_completed = ? WHERE id = ?", (datetime.today().date(), self.id,))
        self.db.commit()
        if self.open:
            self.cur.execute("UPDATE streak SET current_streak = current_streak + 1 WHERE habit_id = ?", (self.id,))
            self.db.commit()
            self.update_longest_streaks()
            self.open = False


    def broken(self):
        """
        Breaks a habit by updating current streak in the database as 0.
        """
        self.cur.execute("UPDATE streak SET current_streak = 0 WHERE habit_id = ?", (self.id,))
        self.db.commit()

    def is_open(self):
        """
        Determines if the habit is open by checking if the last completion is in the current period cycle.
        If the habit has just been created, the habit is set as open.
        If the habit has not been completed in the last expected period cycle, the habit is broken.
        """
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

    def get_due_date(self):
        """
        Determines the due date for a habit by subtracting the days_since_created from the start of the next period cycle.
        :return: Number of days until the habit needs to be completed.
        """
        created = datetime.strptime(self.cur.execute("SELECT created_date FROM habit WHERE id = ?", (self.id,)).fetchone()[0], "%Y-%m-%d").date()
        last = datetime.strptime(self.cur.execute("SELECT last_completed FROM habit WHERE id = ?", (self.id,)).fetchone()[0],"%Y-%m-%d").date()

        days_since_created = (datetime.today().date() - created).days
        current_period_cycle = days_since_created // self.period

        start_of_next_period_cycle = (current_period_cycle + 1) * self.period

        return start_of_next_period_cycle - days_since_created - 1


    def get_current_streak(self):
        """
        Reads the current streak from the streak table in the database.
        :return: Current streak of the habit
        """
        self.cur.execute("SELECT current_streak FROM streak WHERE habit_id = ?", (self.id,))
        return self.cur.fetchone()[0]

    def get_longest_streak(self):
        """
        Reads the longest streak from the streak table in the database.
        :return: Longest streak of the habit
        """
        self.cur.execute("SELECT longest_streak FROM streak WHERE habit_id = ?", (self.id,))
        return self.cur.fetchone()[0]

    def update_longest_streaks(self):
        """
        Updates the longest streak in the streak table in the database
        if the current streak is greater than the longest streak.
        """
        if self.get_current_streak() > self.get_longest_streak():
            self.cur.execute("UPDATE streak SET longest_streak = ? WHERE habit_id = ?", (self.get_current_streak(), self.id,))
            self.db.commit()
from habit import Habit
from db import get_cursor

class HabitManager:
    def __init__(self):
        self.habits = []
        self.db, self.cur = get_cursor()
        self.init_habits()

    def init_habits(self):
        self.cur.execute("SELECT id, name, period, last_completed FROM habit")
        rows = self.cur.fetchall()
        for row in rows:
            self.habits.append(Habit(row[0], row[1], row[2], row[3]))
        for habit in self.habits:
            habit.is_open()

    # Creating a habit by inserting name and period into the habit table.
    # The creation date is added automatically as the current date.
    # Then a new habit class object is created and appended to the habit_manager habit list.
    # A record is created in the streak table, linking habit and streak.
    # longest_streak and current_streak have a default value 0 at the first initialisation
    def create_habit(self, name, period):
        self.cur.execute("INSERT INTO habit (name, period) Values (?, ?)", (name, period))
        self.db.commit()
        habit_id = self.cur.lastrowid
        last_completed = self.cur.execute("SELECT last_completed FROM habit WHERE id = ?", (habit_id,)).fetchone()[0]
        self.habits.append(Habit(habit_id, name, period, last_completed))
        self.cur.execute("INSERT INTO streak (habit_id) VALUES (?)", (habit_id,))
        self.db.commit()

    def delete_habit(self, habit_id):
        self.cur.execute("DELETE FROM habit WHERE id = ?", (habit_id,))
        self.cur.execute("DELETE FROM streak WHERE habit_id = ?", (habit_id,))
        self.cur.execute("DELETE FROM completed WHERE habit_id = ?", (habit_id,))
        self.db.commit()
        for habit in self.habits:
            if habit.id == habit_id:
                self.habits.remove(habit)

    def list_habits(self):
        return self.habits

    def list_open_habits(self):
        return [habit for habit in self.habits if habit.open]

    def list_habits_by_periodically(self):
        return sorted(self.habits, key=lambda h: h.period)

    def get_longest_streaks(self):
        return list(map(lambda h: [h.name, h.get_longest_streak()], self.habits))

    def save_to_db(self):
        pass

    def delete_from_db(self):
        pass

    def close_db(self):
        self.db.close()

    def __repr__(self):
        return '\n'.join(map(repr, self.habits))
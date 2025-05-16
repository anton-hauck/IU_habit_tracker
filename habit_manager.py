from habit import Habit
from db import get_cursor

class HabitManager:
    def __init__(self):
        self.habits = []
        self.db, self.cur = get_cursor()
        self.init_habits()

    def init_habits(self):
        self.cur.execute("SELECT id, name, period FROM habit")
        rows = self.cur.fetchall()
        for row in rows:
            self.habits.append(Habit(row[0], row[1], row[2]))

    # Creating a habit by inserting name and period into the habit table.
    # The creation date is added automatically as the current date.
    # Then a new habit class object is created and appended to the habit_manager habit list.
    # A record is created in the streak table, linking habit and streak.
    # longest_streak and current_streak have a default value 0 at the first initialisation
    def create_habit(self, name, period):
        self.cur.execute("INSERT INTO habit (name, period) Values (?, ?)", (name, period))
        self.db.commit()
        habit_id = self.cur.lastrowid
        self.habits.append(Habit(habit_id, name, period))
        self.cur.execute("INSERT INTO streak (habit_id) VALUES (?)", (habit_id,))
        self.db.commit()

    def delete_habit(self, id):
        self.cur.execute("DELETE FROM habit WHERE id = ?", (id,))
        self.db.commit()
        self.cur.execute("DELETE FROM streak WHERE habit_id = ?", (id,))
        self.db.commit()
        self.cur.execute("DELETE FROM completed WHERE habit_id = ?", (id,))
        self.db.commit()
        for habit in self.habits:
            if habit.id == id:
                self.habits.remove(habit)

    def list_habits(self):
        return self.habits

    # Lists Habits periodically. Since the period is stored as a string, a lambda function is used with a predefined order.
    # In case a period is missing or not in the order, it gets ordered at the end by h.period, 99 <-
    def list_habits_by_periodically(self):
        order = {"Daily": 0, "Weekly": 1, "Monthly": 2}
        ordered_habits = sorted(self.habits, key=lambda h: order.get(h.period, 99))
        return ordered_habits

    def get_longest_streaks(self):
        longest_streak_list = []
        for habit in self.habits:
            longest_streak_list.append([habit.name, habit.get_longest_streak()])
        return longest_streak_list

    def save_to_db(self):
        pass

    def delete_from_db(self):
        pass

    def close_db(self):
        self.db.close()

    def __repr__(self):
        return '\n'.join(map(repr, self.habits))
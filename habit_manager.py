from habit import Habit

"""
The habit_manager_class handles habits. 
It has the purpose to manage functions that relate to several habits. 
"""

class habit_manager_class:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.db, self.cur = db_manager.get_cursor()
        self.habits = []
        self.init_habits()

    def init_habits(self):
        """
        Loads all habits from the database into memory as Habit objects.
        This approach ensures that the app can efficiently interact with habits
        without repeatedly querying the database.
        """
        self.cur.execute("SELECT id, name, period, last_completed FROM habit")
        rows = self.cur.fetchall()
        for row in rows:
            self.habits.append(Habit(row[0], row[1], row[2], row[3], db_manager=self.db_manager))

    def create_habit(self, name, period):
        """
        Creating a habit by inserting name and period into the habit table.
        The creation date is added automatically as the current date.
        Then a new habit class object is created and appended to the habit_manager habit list.
        A record is created in the streak table, linking habit and streak.
        longest_streak and current_streak have a default value 0 at the first initialisation
        :param name: The name of the habit
        :param period: The period of the habit
        """
        self.cur.execute("INSERT INTO habit (name, period) Values (?, ?)", (name, period))
        self.db.commit()
        habit_id = self.cur.lastrowid
        last_completed = self.cur.execute("SELECT last_completed FROM habit WHERE id = ?", (habit_id,)).fetchone()[0]
        self.habits.append(Habit(habit_id, name, period, last_completed, db_manager=self.db_manager))
        self.cur.execute("INSERT INTO streak (habit_id) VALUES (?)", (habit_id,))
        self.db.commit()

    def delete_habit(self, habit_id):
        """
        Deletes a habit from all tables of the database and from the habit list of the habit_manager.
        :param habit_id: The ID of the habit to delete
        """
        self.cur.execute("DELETE FROM habit WHERE id = ?", (habit_id,))
        self.cur.execute("DELETE FROM streak WHERE habit_id = ?", (habit_id,))
        self.cur.execute("DELETE FROM completed WHERE habit_id = ?", (habit_id,))
        self.db.commit()
        for habit in self.habits:
            if habit.id == habit_id:
                self.habits.remove(habit)

    def list_habits(self):
        """
        Lists all habits from the habit_manager
        :return: list of habits
        """
        return self.habits

    def get_habit_names(self):
        """
        Returns a list of habit names from the habit_manager
        :return: List of habitnames
        """
        return [habit.name for habit in self.habits]

    def list_open_habits(self):
        """
        Returns a list of habits from the habit_manager that are open
        :return: List of habits
        """
        return [habit for habit in self.habits if habit.open]

    def list_habits_periodically(self):
        """
        Returns a sorted list of habits from the habit_manager
        :return: Sorted list of habits
        """
        return sorted(self.habits, key=lambda h: h.period)

    def show_list_of_habits_with_x_period(self, period):
        """
        Returns a list of habits from the habit_manager with the given period.
        :param period: The period of the habits
        :return: List of habits with the given period
        """
        habit_list = []
        for habit in self.habits:
            if habit.period == period:
                habit_list.append(habit)
        return habit_list

    def list_longest_streaks(self):
        """
        Returns a list of lists with habit name and it's longest streak
        :return: List of lists
        """
        return list(map(lambda h: [h.name, h.get_longest_streak()], self.habits))

    def get_current_streaks(self):
        """
        Returns a list of lists with habit name and it's current streak
        :return: List of lists
        """
        return list(map(lambda h: [h.name, h.get_current_streak()], self.habits))

    def close_db(self):
        """
        Closes the database connection.
        """
        self.db.close()
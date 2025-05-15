from habit import Habit

class HabitManager:
    def __init__(self, habits: list[Habit]):
        self.habits = habits

    def create_habit(self, name, period):
        pass

    def delete_habit(self, name):
        pass

    def list_habits(self):
        pass

    def list_habits_by_periodically(self):
        pass

    def get_longest_streak(self):
        pass

    def save_to_db(self):
        pass

    def delete_from_db(self):
        pass

    def __repr__(self):
        return '\n'.join(map(repr, self.habits))
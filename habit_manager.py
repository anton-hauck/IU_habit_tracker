from habit import Habit

class HabitManager:
    def __init__(self, habits: list[Habit]):
        self.habits = habits

    def __repr__(self):
        return '\n'.join(map(repr, self.habits))
class Habit:
    def __init__(self, id: int, name: str, created_date: str):
        self.id = id
        self.name = name
        self.created_date = created_date

    def complete(self):
        pass

    def broken(self):
        pass

    def get_current_streak(self):
        pass

    def get_longest_streak(self):
        pass

    def __repr__(self):
        return f"Habit {self.id} {self.name} {self.created_date}"
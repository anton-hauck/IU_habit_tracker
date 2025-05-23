import pytest
import habit_manager
import db


class TestHabitManager:
    def setup_method(self):
        self.db_manager = db.db_manager("test.db", test_environment=True)
        self.habit_manager_object = habit_manager.habit_manager_class(self.db_manager)

    def test_list_open_habits(self):
        habit_list = self.habit_manager_object.list_open_habits()
        assert type(habit_list) == list
        assert len(habit_list) == 5

    def test_complete_habit(self):
        self.habit_manager_object.habits[1].complete()
        habit_list = self.habit_manager_object.list_open_habits()
        assert len(habit_list) == 4

    def test_create_habit(self):
        self.habit_manager_object.create_habit("TestHabit", 15)
        habit_list = self.habit_manager_object.list_habits()
        assert len(habit_list) == 6

    def test_delete_habit(self):
        self.habit_manager_object.delete_habit(6)
        habit_list = self.habit_manager_object.list_habits()
        assert len(habit_list) == 5

    def test_list_habits(self):
        habit_list = self.habit_manager_object.list_habits()
        assert type(habit_list) == list
        assert len(habit_list) == 5

    def test_list_habits_periodically(self):
        habit_list = self.habit_manager_object.list_habits_periodically()
        for x in range(1, 1, len(habit_list)):
            assert type(habit_list[x].period) == int
            assert habit_list[x-1].period < habit_list[x].period

    def test_list_habits_with_period_x(self):
        self.habit_manager_object.create_habit("DailyTestHabit", 1)
        habit_list = self.habit_manager_object.show_list_of_habits_with_x_period(1)
        assert len(habit_list) == 2

    def test_list_current_streaks(self):
        assert self.habit_manager_object.habits[4].get_current_streak() == 0
        self.habit_manager_object.habits[4].complete()
        assert self.habit_manager_object.habits[4].get_current_streak() == 1

    def test_list_longest_streaks(self):
        habit_list = self.habit_manager_object.list_longest_streaks()
        assert len(habit_list) == 5

    def test_get_longest_streak(self):
        assert self.habit_manager_object.habits[3].get_longest_streak() == 7
        self.habit_manager_object.habits[3].complete()
        assert self.habit_manager_object.habits[3].get_longest_streak() == 8


    def teardown_method(self):
        self.habit_manager_object.close_db()
        self.db_manager.close_db()
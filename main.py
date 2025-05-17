# starting the project, interaction with user inputs, printing the cli
import habit
import habit_manager
import db
import sys
import test_db


def main():
    db.create_tables()
    habitManager = habit_manager.HabitManager()
    '''
    habitManager.create_habit("Sport", 7)
    habitManager.create_habit("Call Mama", 1)
    habitManager.create_habit("Car wash", 30)
    habitManager.habits[0].complete()
    habitManager.habits[2].complete()
    habitManager.habits[1].complete()
    habitManager.habits[0].complete()
    habitManager.habits[2].complete()
    habitManager.habits[2].complete()
    habitManager.delete_habit(1)
    '''
    print(habitManager.get_longest_streaks())
    print(habitManager.list_habits_by_periodically())

    habitManager.close_db()
    db.close_db()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        test_db.create_test_tables()
        habitManager = habit_manager.HabitManager()
        print(habitManager)
        print(habitManager.list_open_habits())
        habitManager.close_db()
        db.close_db()
    elif len(sys.argv) > 1 and sys.argv[1].lower() != "test":
        print("There was a typo in your argument")
    else:
        main()
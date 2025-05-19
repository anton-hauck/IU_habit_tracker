# starting the project, interaction with user inputs, printing the cli
import habit
import habit_manager
import db
import sys


def main():
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
    print(habit_manager_object.get_longest_streaks())
    print(habit_manager_object.list_habits_by_periodically())

    habit_manager_object.close_db()
    db_manager.close_db()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        db_manager = db.db_manager("test.db", test_environment=True)
        habit_manager_object = habit_manager.habit_manager_class(db_manager)
        main()
    elif len(sys.argv) > 1 and sys.argv[1].lower() != "test":
        print("There was a typo in your argument")
    else:
        db_manager = db.db_manager()
        # dependency injection of the database manager to the habit manager as an object.
        # Now the database initialised in the db_manager class can be used across the habit_manager
        # and habit class
        habit_manager_object = habit_manager.habit_manager_class(db_manager)
        main()
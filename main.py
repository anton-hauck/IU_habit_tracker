# starting the project, interaction with user inputs, printing the cli
import habit
import habit_manager
import db
import sys


def main():
    db.create_tables()
    habitManager = habit_manager.HabitManager()
    '''
    habitManager.create_habit("Sport", "Weekly")
    habitManager.create_habit("Call Mama", "Daily")
    habitManager.create_habit("Car wash", "Monthly")
    habitManager.delete_habit(1)
    habitManager.habits[0].complete()
    habitManager.habits[2].complete()
    habitManager.habits[1].complete()
    habitManager.habits[0].complete()
    habitManager.habits[2].complete()
    habitManager.habits[2].complete()
    '''

    habitManager.close_db()
    db.close_db()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].lower() == "test":
        print("test")
    elif len(sys.argv) > 1 and sys.argv[1].lower() != "test":
        print("There was a typo in your argument")
    else:
        main()
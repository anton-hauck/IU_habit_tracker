# starting the project, interaction with user inputs, printing the cli
import habit
import habit_manager
import db
import sys
import questionary
import os

# clear console on all os
def clear_console():
    # For Windows
    if os.name == 'nt':
        os.system('cls')
    # For Unix/Linux/Mac
    else:
        os.system('clear')

# helper function to ask for a habit from a habit list input
def ask_for_habit(habit_list):
    choices = [questionary.Choice(title=x.name, value=x) for x in habit_list]
    return questionary.select("Please select a habit:", choices=choices).ask()


def main():
    while True:
        choice = questionary.select(
            "Please select an action:",
            choices=["Show a list of open habits", "Complete a habit", "Create a habit", "Delete a habit", "Analyze habits...", "Exit"],
        ).ask()

        if choice == "Show a list of open habits":
            for x in habit_manager_object.list_open_habits():
                print(x.name)
        elif choice == "Complete a habit":
            selected = ask_for_habit(habit_manager_object.list_habits())
            if questionary.confirm("Do you want to complete habit: " + selected.name).ask():
                next(x for x in habit_manager_object.habits if x.id == selected.id).complete()
        elif choice == "Create a habit":
            name = questionary.text("Enter habit name").ask()
            period = questionary.text("Enter habit period in days", validate=lambda val: val.isdigit() or "Please enter a valid number").ask()
            habit_manager_object.create_habit(name, int(period))
        elif choice == "Delete a habit":
            selected = ask_for_habit(habit_manager_object.list_habits())
            if questionary.confirm("Do you want to delete habit: " + selected.name).ask():
                habit_manager_object.delete_habit(habit_id=selected.id)
        elif choice == "Analyze habits...":
            choice = questionary.select(
                "Please select an action:",
                choices=["Show a list of all habits", "Show a list of all habits with the period X",
                         "Show a list of the longest streaks of all habits",
                         "Show the longest streak of habit X", "Back to main menu"],
            ).ask()
            if choice == "Show a list of all habits":
                for x in habit_manager_object.list_habits():
                    print(x.name)
            elif choice == "Show a list of all habits with the period X":
                pass
            elif choice == "Show a list of the longest streaks of all habits":
                for x in habit_manager_object.list_longest_streaks():
                    print(x[0] + ": Streak: " + str(x[1]))
            elif choice == "Show the longest streak of habit X":
                selected = ask_for_habit(habit_manager_object.list_habits())
                print(selected.name + ": Streak: " + str(next(x for x in habit_manager_object.habits if x.id == selected.id).get_longest_streak()))
            elif choice == "Back to main menu":
                pass
        elif choice == "Exit":
            habit_manager_object.close_db()
            db_manager.close_db()
            break
        else:
            break


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        db_manager = db.db_manager("test.db", test_environment=True)
        habit_manager_object = habit_manager.habit_manager_class(db_manager)
        main()
    elif len(sys.argv) > 1 and sys.argv[1] != "--test":
        print("There was a typo in your argument")
    else:
        db_manager = db.db_manager()
        # dependency injection of the database manager to the habit manager as an object.
        # Now the database initialised in the db_manager class can be used across the habit_manager
        # and habit class
        habit_manager_object = habit_manager.habit_manager_class(db_manager)
        main()
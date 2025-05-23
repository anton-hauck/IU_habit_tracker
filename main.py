# starting the project, interaction with user inputs, printing the cli
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

# helper function to ask for a period from a habit list input
def ask_for_period(habit_list):
    seen = set()
    choices = []
    for habit in habit_list:
        if habit.period not in seen:
            seen.add(habit.period)
            choices.append(questionary.Choice(title=format_days_to_text(habit.period), value=habit.period))
    return questionary.select("Please select a period:", choices=choices).ask()

# helper function to display periods in a more convenient way, as days, weeks and months
def format_days_to_text(period):
    if period == 1:
        return "Daily"
    elif period == 7:
        return "Weekly"
    elif period == 30:
        return "Monthly"
    else:
        return f"{period} days"

# helper function to validate the name when creating a habit
def validate_name(input_text):
    if input_text.startswith(" "):
        return "Please do not start with a space"
    elif input_text.strip() == "":
        return "The habit name cannot be empty."
    elif input_text in habit_manager_object.get_habit_names():
        return "The habit name is already taken."
    else:
        return True

def validate_period(input_text):
    if input_text.startswith(" "):
        return "Please do not start with a space."
    elif input_text.strip() == "":
        return "The habit period cannot be empty."
    elif not input_text.isdigit():
        return "Please enter a valid number (digits only)."
    elif int(input_text) <= 0:
        return "The period must be greater than 0."
    return True

# helper function to rewrite due dates
def rewrite_due_dates(days):
    if days == 0:
        return "due today"
    if days == 1:
        return "due tomorrow"
    if days > 2:
        return f"due in {days} days"



def main():
    print("Welcome to Habit Manager!")
    while True:
        choice = questionary.select(
            "Please select an action:",
            choices=["Show a list of open habits",
                     "Complete a habit",
                     "Create a habit",
                     "Delete a habit",
                     "Analyze habits...",
                     "- Exit"],
        ).ask()

        if choice == "Show a list of open habits":
            for x in habit_manager_object.list_open_habits():
                print(" · " + x.name + " -> " + rewrite_due_dates(x.get_due_date()))
        elif choice == "Complete a habit":
            selected = ask_for_habit(habit_manager_object.list_habits())
            if questionary.confirm("Do you want to complete habit: " + selected.name).ask():
                next(x for x in habit_manager_object.habits if x.id == selected.id).complete()
                print("Habit completed")
            else:
                print("Canceled")
        elif choice == "Create a habit":
            name = questionary.text("Enter habit name",validate=validate_name).ask()
            period_choice = questionary.select("Please choose a period:", choices=["Daily", "Weekly", "Monthly", "Custom"]).ask()
            period = None
            if period_choice == "Custom":
                period = questionary.text("Enter habit period in days", validate=validate_period).ask()
            elif period_choice == "Daily":
                period = 1
            elif period_choice == "Weekly":
                period = 7
            elif period_choice == "Monthly":
                period = 30
            if questionary.confirm("Do you want to create habit: " + name + " with the period: " + str(period)).ask():
                habit_manager_object.create_habit(name, int(period))
                print("Habit created")
            else:
                print("Canceled")
        elif choice == "Delete a habit":
            selected = ask_for_habit(habit_manager_object.list_habits())
            if questionary.confirm("Do you want to delete habit: " + selected.name).ask():
                habit_manager_object.delete_habit(habit_id=selected.id)
                print("Habit deleted")
            else:
                print("Canceled")
        elif choice == "Analyze habits...":
            analyze_submenu = True
            while analyze_submenu:
                choice = questionary.select(
                    "Please select an action:",
                    choices=["Show a list of all habits",
                             "Show a list of all habits periodically sorted",
                             "Show a list of all habits with the period X",
                             "Show a list of the longest streaks of all habits",
                             "Show the longest streak of habit X",
                             "- Back to main menu"],
                ).ask()
                if choice == "Show a list of all habits":
                    for x in habit_manager_object.list_habits():
                        print(" · " + x.name)
                elif choice == "Show a list of all habits periodically sorted":
                    for x in habit_manager_object.list_habits_periodically():
                        print(" · " + x.name + ": Period: " + format_days_to_text(x.period))
                elif choice == "Show a list of all habits with the period X":
                    selected = ask_for_period(habit_manager_object.list_habits())
                    for x in habit_manager_object.show_list_of_habits_with_x_period(selected):
                        print(" · " + x[1])
                elif choice == "Show a list of the longest streaks of all habits":
                    for x in habit_manager_object.list_longest_streaks():
                        print(" · " + x[0] + ": Longest streak: " + str(x[1]))
                elif choice == "Show the longest streak of habit X":
                    selected = ask_for_habit(habit_manager_object.list_habits())
                    print(selected.name + ": Streak: " + str(next(x for x in habit_manager_object.habits if x.id == selected.id).get_longest_streak()))
                elif choice == "- Back to main menu":
                    analyze_submenu = False
                else:
                    print("Sorry, I don't understand that. Please try again.")
        elif choice == "- Exit":
            print("Now exiting...")
            habit_manager_object.close_db()
            db_manager.close_db()
            print("Database closed.")
            print("See you next time. Stay on track with your habits, you are doing great!")
            break
        else:
            print("Sorry, I don't understand that. Please try again.")


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
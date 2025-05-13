# starting the project, interaction with user inputs, printing the cli
import habit
import habit_manager

def main():
    pass

if __name__ == '__main__':
    main()
    habit1 = habit.Habit(1, "Name1", "asdasd")
    habit2 = habit.Habit(2, "Name2", "asdasd")
    habit3 = habit.Habit(3, "Name3", "asdasd")
    habit4 = habit.Habit(4, "Name4", "asdasd")
    habit_Manager = habit_manager.HabitManager([habit1, habit2, habit3, habit4])
    print(habit_Manager)

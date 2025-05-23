# Habit Tracker

This is a habit-tracking application developed as part of the Object-Oriented Programming with Python course for my Bachelor's program at IU. The app helps users manage, track, and analyze their habits effectively using a command-line interface (CLI).

## Features

- **Interactive CLI**: User-friendly text-based interface powered by `questionary`.
- **Validation**: User inputs are validated to not run into errors.
- **Confirm**: Unreversible actions need to be confirmed by the user. 
- **Interactions**:
  - **Show a list of open habits**: List open habits and their due dates.
  - **Complete a habit**: Complete a habit and update streak automatically.
  - **Create a habit**: Create new habits with customizable periods (daily, weekly, monthly, or custom intervals).
  - **Delete a habit**: Deletes a habit.
  - **Analyze habits**:
    - **Show a list of all habits**
    - **Show a list of all habits periodically sorted**
    - **Show a list of all habits with the period X**
    - **Show a list of all current streaks**
    - **Show a list of the longest streaks of all habits**
    - **Show the longest streak of habit X**

---

## Installation

### Prerequisites
- Python 3.7 or higher
- `pip` (Python package manager)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/anton-hauck/IU_habit_tracker.git
   cd IU_habit_tracker
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. Follow the instructions on-screen.


### Testing
To run the application in test mode:
```bash
python main.py --test
```

This will use a temporary test database for isolated testing.

Or use:
```bash
   pytest .
   ```

---

## Project Structure

- **`main.py`**: Entry point of the application. Manages user interaction through the CLI.
- **`habit.py`**: Defines the `Habit` class, encapsulates habit-related logic.
- **`habit_manager.py`**: Manages all habits, including creating, deleting, and listing them.
- **`db.py`**: Initialises the database, or the test-database.
- **`requirements.txt`**: Lists Python dependencies for the project.

---

## Features in Development

- **Cheat token**: Earning consecutive streaks for X-days grants a "Token" that can be used to skip a habit period.
- **GUI**: Switching from a CLI to a GUI.
- **Visualisations**: Analyzing and showing habit completions in form of a graph.

---

## Acknowledgments

This project was developed as part of the IU coursework.
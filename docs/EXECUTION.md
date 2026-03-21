# Execution Guide

## Requirements

To execute the Smart Spaces project, the following requirements are needed:

- **Python 3.13 or higher**
- A terminal or command-line interface
- No external libraries or frameworks are required

The application uses only the Python standard library. Data is persisted in a SQLite database (`smartspaces.db`),
which is also part of the standard library and requires no additional installation.

---

## Setting Up the Database

Before running the application for the first time, the database must be initialized. From the project root:
```bash
python crear_bd.py
```

This script will:

- Create the `smartspaces.db` file at the project root.
- Create all required tables (`spaces`, `meeting_rooms`, `users`, `bookings`).
- Populate them with the initial seed data.

> ⚠️ Running `crear_bd.py` again will **drop and recreate** the database, resetting all data to its initial state.

**To delete the database manually:**
```bash
# Linux / Git Bash
rm smartspaces.db

# Windows CMD
del smartspaces.db
```

---

## How to Execute the Menu

1. Open a terminal.
2. Navigate to the root directory of the project (where the `presentation` folder is located).
3. Ensure the database has been initialized (`smartspaces.db` exists).
4. Run the following command:
```bash
python -m presentation.menu
```

After executing this command, the main menu of the Smart Spaces system will be displayed.

---

## Main Menu Options

Once the application is running, the user can interact with the system through the following options:

1. List spaces
2. List users
3. List bookings
4. Create booking
5. Cancel booking
6. Finish booking
7. Create space
8. List available spaces
9. Modify booking
10. Exit

Each option is selected by typing its number and pressing Enter.

---

## Running Tests

### Running the Test Suite

All tests are located in the `tests/` directory and use Python's built-in `unittest` module. From the project root
(`SmartSpaces/`), run:
```bash
# Run all tests
python -m unittest discover -s tests -t .

# Run a specific test module (for example, Booking)
python -m unittest tests.domain.test_booking
```

A successful run will output something like:
```
....................
----------------------------------------------------------------------
Ran 28 tests in 0.006s

OK
```

### Running Tests with Coverage

To measure and report test coverage, follow this sequence:

**Step 1 — Install dependencies** (including `coverage`):
```bash
pip install -r requirements.txt
```

> If `coverage` is not yet in `requirements.txt`, install it directly with `pip install coverage`.

**Step 2 — Run the test suite under `coverage`:**
```bash
coverage run -m unittest discover -s tests -t .
```

**Step 3 — Display the coverage report in the terminal:**
```bash
coverage report
```

**Step 4 (optional) — Generate an HTML report** for line-by-line visualisation:
```bash
coverage html
```

This creates an `htmlcov/` directory. Open `htmlcov/index.html` in your browser to browse results interactively,
with covered and uncovered lines highlighted.

> **Tip:** Add `htmlcov/` and `.coverage` to your `.gitignore` to avoid committing generated coverage artefacts.

---

## Example Execution Flows

### Example 1: Listing Spaces

1. Start the application.
2. Select option `1` (List spaces).
3. The system displays all registered spaces, including:
    - Space ID
    - Name
    - Type of space
    - Status
    - Capacity
4. If a space belongs to a specialized type (e.g. meeting room), its specific attributes such as room number, floor,
   power outlets, and equipment are also shown.

### Example 2: Creating a Booking

1. Select option `4` (Create booking).
2. Enter a valid User ID.
3. Enter a valid Space ID.
4. Enter the start and end date and time using one of the accepted formats:
    - `YYYY-MM-DD HH:MM`
    - `YYYY/MM/DD HH:MM`
5. The system checks:
    - Space availability
    - Booking overlaps
    - Validity of the user and space
6. If all rules are satisfied, the booking is created and persisted in the database.

### Example 3: Canceling a Booking

1. Select option `5` (Cancel booking).
2. Enter the booking ID.
3. If the booking exists and is active, it is cancelled and the database is updated.
4. The system confirms the cancellation.

### Example 4: Finishing a Booking

1. Select option `6` (Finish booking).
2. Enter the booking ID.
3. The booking status is updated to finished in the database.
4. The system confirms the operation.

---

## Error Handling During Execution

If the user performs an invalid action (such as entering an incorrect date format, selecting a non-existent ID, or
attempting an invalid booking), the system will:

- Reject the operation.
- Display an explanatory error message.
- Return safely to the main menu.

---

## Execution Notes

- Data is persisted in `smartspaces.db` and survives between executions.
- Run `python crear_bd.py` to reset all data to its initial state.
- The system is designed for single-user, sequential interaction.
- To exit the application safely, select option `10` (Exit).

## Summary

The Smart Spaces menu provides a simple, guided way to interact with the system, allowing users to explore spaces,
manage bookings, and validate the system's behavior through a clear command-line interface. All data is durably
persisted in a SQLite relational database.
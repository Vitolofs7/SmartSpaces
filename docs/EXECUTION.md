# Execution Guide

## Requirements

To execute the Smart Spaces project, the following requirements are needed:

- **Python 3.13 or higher**
- A terminal or command-line interface
- **Flask** (`pip install flask`) — required only for the web interface

The application uses only the Python standard library for the console menu. Data is persisted in a SQLite database
(`smartspaces.db`), which is also part of the standard library and requires no additional installation.

---

## Setting Up the Database

Before running the application for the first time, the database must be initialized. From the project root:
```bash
python create_db.py
```

This script will:

- Create the `smartspaces.db` file at the project root.
- Create all required tables (`spaces`, `meeting_rooms`, `users`, `bookings`).
- Populate them with the initial seed data.

> ⚠️ Running `create_db.py` again will **drop and recreate** the database, resetting all data to its initial state.

**To delete the database manually:**
```bash
# Linux / Git Bash
rm smartspaces.db

# Windows CMD
del smartspaces.db
```

---

## How to Execute the Console Menu

1. Open a terminal.
2. Navigate to the root directory of the project (where the `presentation` folder is located).
3. Ensure the database has been initialized (`smartspaces.db` exists).
4. Run the following command:
```bash
python -m presentation.menu
```

After executing this command, the main menu of the Smart Spaces system will be displayed.

---

## How to Execute the Web Interface (Flask)

Smart Spaces also includes a REST API built with Flask, following the **POST-Redirect-GET** pattern for write
operations.

1. Ensure the database has been initialized (`smartspaces.db` exists).
2. From the project root, start the server:
```bash
python -m presentation.app
```
3. Open `http://localhost:5000` in your browser, or interact via `curl`.

### Available Routes

#### 📥 Read (GET)

| Route | Description |
|-------|-------------|
| `GET /` | Welcome page with links to main endpoints |
| `GET /users` | List all users |
| `GET /users/<user_id>` | Get a specific user |
| `GET /spaces` | List all spaces |
| `GET /spaces/<space_id>` | Get a specific space |
| `GET /bookings` | List all bookings |
| `GET /bookings/<booking_id>` | Get a specific booking |
| `GET /spaces/disponibles/<fecha_inicio>/<fecha_fin>` | Available spaces in a date range (ISO 8601) |
| `GET /bookings/usuario/<user_name>` | Bookings for a specific user |
| `GET /bookings/espacio/<space_name>` | Bookings for a specific space |

#### ➕ Create (POST with redirect)

| Route | Description |
|-------|-------------|
| `POST /users/nuevo/<user_id>/<name>/<surname1>/<surname2>` | Create a new user |
| `POST /spaces/nuevo/<space_name>/<int:capacity>/<space_type>` | Create a new space |
| `POST /spaces/nueva-sala/<name>/<capacity>/<room>/<floor>/<outlets>` | Create a meeting room |
| `POST /bookings/nueva/<user>/<space>/<fecha_inicio>/<fecha_fin>` | Create a new booking |

#### 🔄 Status Changes (POST with redirect)

| Route | Description |
|-------|-------------|
| `POST /bookings/<booking_id>/cancelar` | Cancel a booking |
| `POST /bookings/<booking_id>/finalizar` | Mark a booking as finished |
| `POST /bookings/<booking_id>/reprogramar/<nueva_inicio>/<nueva_fin>` | Reschedule a booking |

#### 🚫 Deactivation (POST with redirect)

| Route | Description |
|-------|-------------|
| `POST /users/<user_id>/desactivar` | Deactivate a user |

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| `200 OK` | Successful operation (GET) |
| `302 Found` | Redirect after POST (POST-Redirect-GET pattern) |
| `400 Bad Request` | Invalid data (malformed date, inactive user, etc.) |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | Duplicate resource or state conflict |
| `500 Internal Server Error` | Unexpected server error |

---

## Main Menu Options

Once the console application is running, the user can interact with the system through the following options:

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

### Example 5: Creating a Booking via Web API

```bash
curl -X POST http://localhost:5000/bookings/nueva/user1/space2/2025-06-01T09:00/2025-06-01T11:00
```

The server responds with a `302` redirect to `GET /bookings/<new_booking_id>`, returning the created booking as JSON.

### Example 6: Listing Available Spaces via Web API

```bash
curl http://localhost:5000/spaces/disponibles/2025-06-01T09:00/2025-06-01T11:00
```

Returns a JSON list of spaces with no overlapping bookings in the given time range.

---

## Error Handling During Execution

If the user performs an invalid action (such as entering an incorrect date format, selecting a non-existent ID, or
attempting an invalid booking), the system will:

- **Console menu**: reject the operation, display an explanatory error message, and return safely to the main menu.
- **Web API**: return the appropriate HTTP error code (`400`, `404`, `409`, or `500`) with a JSON error description.

---

## Execution Notes

- Data is persisted in `smartspaces.db` and survives between executions.
- Run `python create_db.py` to reset all data to its initial state.
- The console menu is designed for single-user, sequential interaction.
- The Flask web interface can serve multiple requests but is intended for development/demo use; it runs Flask's
  built-in server, which is not suitable for production deployments.
- To exit the console application safely, select option `10` (Exit).
- To stop the Flask server, press `Ctrl+C` in the terminal.

## Summary

Smart Spaces offers two ways to interact with the system:

- **Console menu** — a simple, guided command-line interface for exploring spaces, managing bookings, and validating
  system behavior.
- **Flask web interface** — a REST API exposing all core operations over HTTP, suitable for integration with other
  tools or front-end clients.

All data is durably persisted in a SQLite relational database regardless of which interface is used.
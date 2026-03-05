# Tests and Steps - Smart Spaces

This document describes how to run the project's tests and what each of them validates.

---

## 1. Running the Tests

All tests are written using Python's `unittest` module and are located in the `tests/` directory.

### 1.1 Requirements

- Python >= 3.13
- Virtual environment (optional but recommended)
- Installed dependencies (if any)

### 1.2 Commands to Run Tests

From the project root (`SmartSpaces/`):

```bash
    # Run all tests
    python -m unittest discover -s tests -t .
    
    # Run a specific test (for example, Booking)
    python -m unittest tests.domain.test_booking
````

> Note: The `-s tests -t .` option specifies the base directory to search for tests (`-s`) and the root directory for
> imports (`-t .`).

### 1.3 Expected Result

* All tests should run and pass, showing something like:

```
....................
----------------------------------------------------------------------
Ran 28 tests in 0.006s

OK
```

* If any test fails, a `FAIL` or `ERROR` will be displayed with the Python traceback.

---

## 2. Test Structure

Tests are divided into **unit tests** and **integration tests**.

### 2.1 Unit Tests

Location: `tests/domain/`

#### 2.1.1 `test_booking.py`

* **Test Classes**:

    * `FakeUser`, `FakeSpace`, `FakeBookingRepo` (mocks)
    * `TestBooking` (test cases)

* **What it validates**:

    * Creation of valid and invalid bookings.
    * Cancellation and finishing of bookings.
    * Detection of overlapping bookings.
    * Rescheduling of active bookings.
    * Validation of inactive users and unavailable spaces.
    * Space status (`reserved`/`available`) after booking operations.

#### 2.1.2 `test_space.py`

* **Test Class**: `TestSpace`
* **What it validates**:

    * Creation of spaces with valid values.
    * Errors when creating spaces with empty ID or name, or invalid capacity.
    * Property setters and getters (`space_name`, `capacity`, etc.).
    * State methods: `is_available()`, `is_reserved()`, `reserve()`, `release()`, `set_maintenance()`.
    * Validation of invalid state transitions.
    * Status display (`get_space_status_display()`).

#### 2.1.3 `test_user.py`

* **Test Class**: `TestUser`
* **What it validates**:

    * Creation of valid and invalid users.
    * Properties: `full_name()`, `max_active_bookings`, `max_booking_duration`.
    * Activation/deactivation of users.
    * Method `can_make_booking()`.

### 2.2 Integration Tests

Location: `tests/domain/test_integration.py`

#### 2.2.1 `TestIntegrationBookingSystem`

* **What it validates**:

    * Complete booking flow with multiple users and spaces.
    * Creation of bookings and unique ID assignment.
    * Cancellation, finishing, and rescheduling of bookings.
    * Validation of inactive users and spaces in maintenance.
    * Checks that reserved or maintenance spaces cannot be booked.
    * Flow of multiple overlapping bookings and correct space state updates.

---

## 3. Recommendations and Steps to Follow

1. Activate the virtual environment:

```bash
    python -m venv .venv
    source .venv/Scripts/activate  # Windows
    source .venv/bin/activate      # macOS/Linux
```

2. Install dependencies (if added later):

```bash
    pip install -r requirements.txt
```

3. Run all tests regularly to ensure system integrity.

4. After changes in the domain, services, or presentation layers, **check test coverage** and ensure no errors appear.

5. Review `unittest` logs in case of failures and follow the traceback to fix issues.

---

## 4. Test Coverage

* `Booking` → 93–100%
* `Space` → 94–100%
* `User` → 97–100%
* Integration → validates the full booking flow in realistic simulated scenarios.

### 4.1 How to Reproduce Coverage Results

To measure and display the coverage figures shown above, follow this complete sequence from the project root (
`SmartSpaces/`):

**Step 1 — Install dependencies** (including `coverage`):

```bash
pip install -r requirements.txt
```

> Make sure `coverage` is listed in `requirements.txt`. If not, you can install it directly with `pip install coverage`.

**Step 2 — Run the test suite under `coverage`:**

```bash
coverage run -m unittest discover -s tests -t .
```

This executes all tests and records which lines of code are exercised.

**Step 3 — Display the coverage report in the terminal:**

```bash
coverage report
```

You will see a table like:

```
Name                                Stmts   Miss  Cover
-------------------------------------------------------
src/domain/booking.py                  45      2    96%
src/domain/space.py                    38      1    97%
src/domain/user.py                     31      1    97%
tests/domain/test_booking.py           72      0   100%
tests/domain/test_space.py             58      0   100%
tests/domain/test_user.py             44      0   100%
tests/domain/test_integration.py       61      0   100%
-------------------------------------------------------
TOTAL                                 349      4    99%
```

**Step 4 (optional) — Generate an HTML report** for detailed, line-by-line visualisation:

```bash
coverage html
```

This creates an `htmlcov/` directory. Open `htmlcov/index.html` in your browser to browse coverage results
interactively, with covered and uncovered lines highlighted.

> **Tip:** Add `htmlcov/` and `.coverage` to your `.gitignore` to avoid committing generated coverage artefacts.

---

## 5. Final Notes

* All tests are designed to run **in memory**, without relying on databases or external services.
* It is recommended to run the tests before any deployment or integration of new features.

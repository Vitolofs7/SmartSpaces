# Initial Data - Smart Spaces

This document describes the initial seed data provided by `crear_bd.py`, what data it includes, and how
to modify it for testing or demo purposes.

---

## 1. Purpose

The `crear_bd.py` script creates the SQLite database (`smartspaces.db`) and populates all tables with sample data.
This allows running the application with preloaded entities without requiring manual creation through the menu.

---

## 2. Seeded Data

### 2.1 Spaces

The following spaces are seeded into the `spaces` and `meeting_rooms` tables:

| ID | Name               | Type        | Capacity | Extra Info / Equipment                   |
|----|--------------------|-------------|----------|------------------------------------------|
| S1 | Conference Room    | Basic       | 5        | -                                        |
| S2 | Open Space         | Basic       | 10       | -                                        |
| S3 | Main Meeting Room  | Meeting room | 8       | Room 101, floor 1, Projector, Whiteboard |
| S4 | Small Meeting Room | Meeting room | 4       | Room 102, floor 1, TV                    |
| S5 | Private Office     | Private     | 2        | -                                        |

- `Space` instances are stored only in the `spaces` table.
- `SpaceMeetingRoom` instances are stored in both `spaces` and `meeting_rooms`, linked by `space_id`.
- `equipment_list` is stored as a comma-separated TEXT string (e.g. `"Projector,Whiteboard"`).

---

### 2.2 Users

The following users are seeded into the `users` table:

| ID | First Name | Last Name 1 | Last Name 2 | Active |
|----|------------|-------------|-------------|--------|
| U1 | Alice      | Smith       | Johnson     | Yes    |
| U2 | Bob        | Brown       | Taylor      | Yes    |
| U3 | Charlie    | Wilson      | Anderson    | Yes    |
| U4 | Diana      | Martinez    | Lopez       | Yes    |
| U5 | Eve        | Davis       | Clark       | Yes    |

- All users are **active** by default (`active = 1`).
- Users can make bookings according to domain rules (`max_active_bookings = 1`, `max_booking_duration = 2 hours`).

---

### 2.3 Bookings

Sample bookings are seeded into the `bookings` table:

| Booking ID | User ID | Space ID | Start Time           | End Time             | Status |
|------------|---------|----------|----------------------|----------------------|--------|
| B1         | U1      | S1       | Now + 1 hour         | Now + 2 hours        | ACTIVE |
| B2         | U2      | S3       | Tomorrow (same time) | Tomorrow + 2 hours   | ACTIVE |
| B3         | U3      | S2       | Now + 3 hours        | Now + 5 hours        | ACTIVE |

- Datetimes are stored as ISO 8601 TEXT strings.
- Spaces S1, S2, and S3 are set to `RESERVED` status after seeding.

---

## 3. How to Use the Seed Data

### 3.1 Initialize the Database
```bash
python crear_bd.py
```

This recreates the database from scratch and loads all seed data.

### 3.2 Reset to Initial State
```bash
python crear_bd.py
```

Running the script again drops and recreates the database, restoring all data to its initial state.

---

### 3.3 Modifying Data for Tests or Demos

To add data directly via SQL, open the database with the SQLite CLI:
```bash
sqlite3 smartspaces.db
```

- **Add a new user**:
```sql
INSERT INTO users VALUES ('U6', 'Frank', 'Miller', 'Evans', 1);
```

- **Add a new space**:
```sql
INSERT INTO spaces VALUES ('S6', 'Brainstorm Room', 6, 'Basic', 'AVAILABLE');
```

- **Add a meeting room**:
```sql
INSERT INTO spaces VALUES ('S7', 'Board Room', 10, 'Meeting room', 'AVAILABLE');
INSERT INTO meeting_rooms VALUES ('S7', '201', 2, 'Projector,TV', 6);
```

- **Add a booking**:
```sql
INSERT INTO bookings VALUES ('B4', 'S6', 'U6', '2026-04-01T09:00:00', '2026-04-01T11:00:00', 'ACTIVE');
```

> ⚠️ Always insert into `spaces` before `meeting_rooms` or `bookings` to satisfy FOREIGN KEY constraints.

---

## 4. Notes

- Seed data persists between executions since it is stored in `smartspaces.db`.
- Run `python crear_bd.py` to reset all data to its initial state.
- The `equipment_list` field uses comma-separated values; use `.split(",")` in Python to recover the list.
- `PRAGMA foreign_keys = ON` is required on every connection to enforce referential integrity.
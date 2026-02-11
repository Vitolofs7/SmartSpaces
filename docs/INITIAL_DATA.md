# Initial Data - Smart Spaces

This document describes the initial seed data provided by `infrastructure/seed_data.py`, what data it includes, and how
to modify it for testing or demo purposes.

---

## 1. Purpose

The `seed_data()` functions populate the in-memory repositories (`SpaceMemoryRepository`, `UserMemoryRepository`,
`BookingMemoryRepository`) with sample data.  
This allows running the application or tests with preloaded entities without requiring manual creation.

---

## 2. Seeded Data

### 2.1 Spaces

The following spaces are seeded:

| ID | Name               | Type        | Capacity | Extra Info / Equipment                   |
|----|--------------------|-------------|----------|------------------------------------------|
| S1 | Conference Room    | Basic       | 5        | -                                        |
| S2 | Open Space         | Basic       | 10       | -                                        |
| S3 | Main Meeting Room  | MeetingRoom | 8        | Room 101, floor 1, Projector, Whiteboard |
| S4 | Small Meeting Room | MeetingRoom | 4        | Room 102, floor 1, TV                    |
| S5 | Private Office     | Private     | 2        | -                                        |

- `Space` is a generic room or office.
- `SpaceMeetingroom` includes additional attributes like room number, floor, and equipment.

---

### 2.2 Users

The following users are seeded:

| ID | First Name | Last Name 1 | Last Name 2 |
|----|------------|-------------|-------------|
| U1 | Alice      | Smith       | Johnson     |
| U2 | Bob        | Brown       | Taylor      |
| U3 | Charlie    | Wilson      | Anderson    |
| U4 | Diana      | Martinez    | Lopez       |
| U5 | Eve        | Davis       | Clark       |

- All users are **active** by default.
- Users can make bookings according to domain rules (`max_active_bookings = 1`, `max_booking_duration = 2 hours`).

---

### 2.3 Bookings

Sample bookings are created for the seeded users and spaces:

| User ID | Space ID | Start Time           | End Time           |
|---------|----------|----------------------|--------------------|
| U1      | S1       | Now + 1 hour         | Now + 2 hours      |
| U2      | S3       | Tomorrow (same time) | Tomorrow + 2 hours |
| U3      | S2       | Now + 3 hours        | Now + 5 hours      |

- Bookings are created using the `Booking.create(space, user, start, end, repo)` factory.
- These bookings respect overlapping rules, space availability, and active user status.

---

## 3. How to Use the Seed Data

### 3.1 Seeding Repositories

```python
from infrastructure.seed_data import seed_all
from infrastructure.space_memory_repository import SpaceMemoryRepository
from infrastructure.user_memory_repository import UserMemoryRepository
from infrastructure.booking_memory_repository import BookingMemoryRepository

space_repo = SpaceMemoryRepository()
user_repo = UserMemoryRepository()
booking_repo = BookingMemoryRepository()

seed_all(space_repo, user_repo, booking_repo)
````

* This populates all repositories with sample spaces, users, and bookings.

---

### 3.2 Modifying Data for Tests or Demos

* **Add a new user**:

```python
from domain.user import User

user_repo.save(User("U6", "Frank", "Miller", "Evans"))
```

* **Add a new space**:

```python
from domain.space import Space

space_repo.save(Space("S6", "Brainstorm Room", 6, "Basic"))
```

* **Add a booking**:

```python
from datetime import datetime, timedelta
from domain.booking import Booking

user = user_repo.get("U6")
space = space_repo.get("S6")
start = datetime.now() + timedelta(days=1)
end = start + timedelta(hours=2)
Booking.create(space, user, start, end, booking_repo)
```

* **Modify existing bookings**:

    * Retrieve booking from `booking_repo.list()`.
    * Call `reschedule(new_start, new_end, booking_repo)` or `cancel()`.

* **Reset seed data**:

    * Clear repositories with `.clear()` (if implemented) and call `seed_all()` again.

--- 

## 4. Notes

* Seed data is **in-memory only**; it resets on application restart.
* Use `seed_all()` before running tests or demos to ensure consistent state.
* Modify IDs, names, or booking times to simulate different scenarios without affecting other tests.
# Business Rules

This document describes the **business rules implemented in the domain layer** of the Smart Spaces project. These rules
define the valid behavior of users, spaces, and bookings, and ensure the system remains in a consistent and valid state.

Business rules are enforced mainly through:

- Domain entities and value validations
- Controlled state transitions
- Explicit exceptions (`ValueError`) when rules are violated
- Referential integrity constraints enforced by the SQLite database (`FOREIGN KEY`, `NOT NULL`, `PRIMARY KEY`)

---

## General Principles

- All entities must be created in a valid state.
- Invalid operations are prevented at the domain level.
- State changes follow a defined lifecycle.
- Any rule violation results in a `ValueError`.
- All data is persisted in a SQLite relational database (`smartspaces.db`).

---

## Space Rules

### Space Creation

- Every space must have:
    - A unique ID (assigned automatically by the repository)
    - A non-empty name
    - A capacity greater than zero
- Each space has a **type**, defined by its class or overridden attribute.
- Spaces are persisted in the `spaces` table.

### Space Status

- A space can be in one of the following states:
    - AVAILABLE
    - RESERVED
    - MAINTENANCE
- Space status is stored as TEXT in the database and kept in sync with the domain object on every state transition.
- A space under MAINTENANCE cannot be reserved.
- A RESERVED space can still accept non-overlapping bookings.

---

## Meeting Room Specific Rules

Meeting rooms extend the base `Space` class and introduce additional constraints.

### Meeting Room Attributes

- `room_number` must be defined and non-empty.
- `floor` must be a valid non-negative integer.
- `num_power_outlets` must be zero or greater.
- `equipment_list` must be a list of strings; stored in the database as a comma-separated TEXT value.

### Encapsulation Rules

- Internal attributes are private.
- Equipment list is exposed as a copy to prevent external modification.
- Equipment can only be modified through domain methods (`add_equipment`, `remove_equipment`).

### Persistence Rules

- Meeting rooms require two database rows: one in `spaces` (common attributes) and one in `meeting_rooms` (specific attributes).
- The `meeting_rooms` table references `spaces` via a FOREIGN KEY on `space_id`.
- A meeting room row in `meeting_rooms` cannot exist without a corresponding row in `spaces`.

---

## User Rules

### User State

- Users are active by default (`active = 1` in the database).
- Only active users can create bookings.
- Deactivated users have `active = 0` in the database.

### User Identity

- Each user must have:
    - A unique ID (PRIMARY KEY in the `users` table)
    - A non-empty name, surname1, and surname2
- Full name is derived from user attributes and not stored redundantly.

---

## Booking Rules

### Booking Creation

A booking can only be created if:

- The user exists and is active.
- The space exists.
- The start time is strictly before the end time.
- The space is not under MAINTENANCE.
- There are no overlapping active bookings for the same space.

### Booking Time Rules

- Booking start and end times must be valid `datetime` values.
- Datetimes are stored in the database as ISO 8601 TEXT strings.
- Overlapping bookings for the same space are not allowed.

### Booking States

A booking can have the following states:

- ACTIVE
- CANCELLED
- FINISHED

### State Transitions

- An ACTIVE booking can be:
    - Cancelled
    - Finished
- A CANCELLED or FINISHED booking cannot be modified further.

---

## Booking Cancellation Rules

- Only ACTIVE bookings can be cancelled.
- A booking that is already CANCELLED or FINISHED cannot be cancelled again.
- Cancelling a booking releases the associated space.
- The booking status is updated to `CANCELLED` in the database.

---

## Booking Completion Rules

- Only ACTIVE bookings can be finished.
- Finishing a booking changes its status and frees the space.
- Finished bookings are immutable.
- The booking status is updated to `FINISHED` in the database.

---

## Space Availability Rules

- A space is considered unavailable if:
    - It has an active booking during the requested interval.
    - It is explicitly marked as MAINTENANCE.
- Space availability is always checked before confirming a booking.
- RESERVED status does not block future non-overlapping bookings.

---

## Database Integrity Rules

- `PRAGMA foreign_keys = ON` is enabled on every database connection to enforce referential integrity.
- A booking cannot reference a space or user that does not exist in the database.
- A meeting room row cannot exist without its corresponding space row.
- All required fields (`space_name`, `capacity`, `user_id`, etc.) are declared `NOT NULL` in the schema.

---

## Error Handling Rules

- All business rule violations raise a `ValueError`.
- Errors are propagated to the presentation layer.
- The system never silently ignores invalid operations.
- Database integrity errors (`sqlite3.IntegrityError`) are treated as unrecoverable and propagated.

---

## Summary

The business rules ensure that:

- Spaces cannot be double-booked.
- Invalid data cannot enter the system.
- State transitions are consistent and predictable.
- Domain logic remains independent of UI or infrastructure concerns.
- All state is durably persisted in a relational database with enforced integrity constraints.

These rules form the core of the Smart Spaces system and guarantee correct and reliable behavior.
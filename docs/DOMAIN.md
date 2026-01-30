# Domain Layer

## Class: Space

Represents a reservable physical space within the organization, such as a classroom, meeting room, or workstation.

### Attributes

| Attribute      | Type | Privacy   | Description                                                          |
|----------------|------|-----------|----------------------------------------------------------------------|
| `__space_id`   | str  | Private   | Unique identifier of the space.                                      |
| `__space_name` | str  | Private   | Name of the space.                                                   |
| `__capacity`   | int  | Private   | Maximum number of people allowed.                                    |
| `_status`      | str  | Protected | Current state of the space (`AVAILABLE`, `RESERVED`, `MAINTENANCE`). |
| `_bookings`    | dict | Protected | Stores reservations associated with this space.                      |

### Status Constants

- `STATUS_AVAILABLE` — Space is free to reserve.
- `STATUS_RESERVED` — Space is currently reserved.
- `STATUS_MAINTENANCE` — Space is under maintenance and cannot be reserved.

### Methods

| Method                 | Description                                                                                  |
|------------------------|----------------------------------------------------------------------------------------------|
| `space_id`             | Getter for the space identifier.                                                             |
| `space_id`(setter)     | Setter for the space identifier.                                                             |
| `space_name`           | Getter for the space name.                                                                   |
| `space_name`(setter)   | Setter for the space name.                                                                   |
| `capacity`             | Getter for the capacity.                                                                     |
| `capacity`(setter)     | Setter for the capacity.                                                                     |
| `status`               | Getter for the current status.                                                               |
| `status`(setter)       | Setter for the status, validates allowed values (`AVAILABLE`, `RESERVED`, `MAINTENANCE`).    |
| `is_available()`       | Returns `True` if the space is available for reservation.                                    |
| `is_reserved()`        | Returns `True` if the space is reserved.                                                     |
| `reserve()`            | Changes the status to `RESERVED` if currently available. Raises `ValueError` otherwise.      |
| `release()`            | Changes the status back to `AVAILABLE` if currently reserved. Raises `ValueError` otherwise. |
| `set_maintenance()`    | Changes the status to `MAINTENANCE`.                                                         |
| `get_status_display()` | Returns a human-readable description of the current status.                                  |

### Notes

- The class enforces **basic domain rules** (e.g., cannot reserve an already reserved space).
- Future extensions: handling time-based bookings, adding equipment or restrictions via inheritance, etc.
- Status is encapsulated to prevent invalid manual changes outside the class methods.

## Class: Booking

Represents a reservation of a physical space by a user during a specific time interval.
It is a core domain entity responsible for maintaining the consistency and validity of a reservation, including its
lifecycle and time-related rules.

### Attributes

| Attribute    | Type       | Visibility | Description                       |
|--------------|------------|------------|-----------------------------------|
| `booking_id` | `str`      | private    | Unique identifier of the booking. |
| `space`      | `Space`    | protected  | Space being reserved.             |
| `user`       | `User`     | protected  | User who made the reservation.    |
| `start_time` | `datetime` | protected  | Reservation start time.           |
| `end_time`   | `datetime` | protected  | Reservation end time.             |
| `status`     | `str`      | protected  | Current status of the booking.    |

### Status Constants

- `STATUS_ACTIVE` — The booking is currently active.
- `STATUS_CANCELLED` — The booking has been cancelled.
- `STATUS_FINISHED` — The booking has been completed.

### Methods

| Method                         | Description                                                                   |
|--------------------------------|-------------------------------------------------------------------------------|
| `booking_id`                   | Returns the unique booking identifier.                                        |
| `status`                       | Returns the current booking status.                                           |
| `is_active()`                  | Returns `True` if the booking is active.                                      |
| `duration()`                   | Returns the duration of the booking (`end_time - start_time`).                |
| `cancel()`                     | Cancels the booking if it is active. Raises `ValueError` otherwise.           |
| `finish()`                     | Marks the booking as finished if it is active. Raises `ValueError` otherwise. |
| `overlaps_with(other_booking)` | Returns `True` if the time interval overlaps with another booking.            |

## Class: User

Represents a user who reserve spaces

### Attributes

| Attribute              | Type       | Visibility | Description |
|------------------------|------------|------------|-------------|
| `user_id`              | `str`      | private    |             |
| `name`                 | `str`      | protected  |             |
| `active`               | `boolean`  | protected  |             |
| `max_active_bookings`  | `int`      | protected  |             |
| `max_booking_duration` | `datetime` | protected  |             |

### Methods

| Method                   | Description                           |
|--------------------------|---------------------------------------|
| `user_id`                |                                       |
| `name`                   |                                       |
| `is_active()`            | Returns `True` if the user is active. |
| `desactivate()`          |                                       |
| `can_make_booking()`     |                                       |
| `max_active_bookings()`  |                                       |
| `max_booking_duration()` |                                       |
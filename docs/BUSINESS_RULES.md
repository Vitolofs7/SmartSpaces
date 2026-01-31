# Business Rules

This document describes the **business rules implemented in the domain layer** of the Smart Spaces project. These rules
define the valid behavior of users, spaces, and bookings, and ensure the system remains in a consistent and valid state.

Business rules are enforced mainly through:

- Domain entities and value validations
- Controlled state transitions
- Explicit exceptions (`ValueError`) when rules are violated

---

## General Principles

- All entities must be created in a valid state.
- Invalid operations are prevented at the domain level.
- State changes follow a defined lifecycle.
- Any rule violation results in a `ValueError`.

---

## Space Rules

### Space Creation

- Every space must have:
    - A non-empty ID
    - A non-empty name
    - A capacity greater than zero
- Each space has a **type**, defined by its class or overridden attribute.

### Space Status

- A space can be in one of the following states:
    - AVAILABLE
    - RESERVED
    - MAINTENANCE
- A space cannot be reserved if it is not AVAILABLE.

---

## Meeting Room Specific Rules

Meeting rooms extend the base `Space` class and introduce additional constraints.

### Meeting Room Attributes

- `room_number` must be defined and non-empty.
- `floor` must be a valid integer.
- `num_power_outlets` must be zero or greater.
- `equipment_list` must be a list of strings.

### Encapsulation Rules

- Internal attributes are private.
- Equipment list is exposed as a copy to prevent external modification.
- Equipment can only be modified through domain methods (`add_equipment`, `remove_equipment`).

---

## User Rules

### User State

- Users are active by default.
- Only active users can create bookings.

### User Identity

- Each user must have:
    - A unique ID
    - A name
- Full name is derived from user attributes and not stored redundantly.

---

## Booking Rules

### Booking Creation

A booking can only be created if:

- The user exists and is active.
- The space exists.
- The start time is strictly before the end time.
- The space is available for the requested time interval.
- There are no overlapping bookings for the same space.

### Booking Time Rules

- Booking start and end times must be valid `datetime` values.
- Overlapping bookings for the same space are not allowed.

### Booking States

A booking can have the following states:

- ACTIVE
- CANCELED
- FINISHED

### State Transitions

- An ACTIVE booking can be:
    - Canceled
    - Finished
- A CANCELED or FINISHED booking cannot be modified further.

---

## Booking Cancellation Rules

- Only existing bookings can be canceled.
- A booking that is already canceled or finished cannot be canceled again.
- Canceling a booking releases the associated space.

---

## Booking Completion Rules

- Only ACTIVE bookings can be finished.
- Finishing a booking changes its status and frees the space.
- Finished bookings are immutable.

---

## Space Availability Rules

- A space is considered unavailable if:
    - It has an active booking during the requested interval.
    - It is explicitly marked as unavailable by its status.
- Space availability is always checked before confirming a booking.

---

## Error Handling Rules

- All business rule violations raise a `ValueError`.
- Errors are propagated to the presentation layer.
- The system never silently ignores invalid operations.

---

## Summary

The business rules ensure that:

- Spaces cannot be double-booked.
- Invalid data cannot enter the system.
- State transitions are consistent and predictable.
- Domain logic remains independent of UI or infrastructure concerns.

These rules form the core of the Smart Spaces system and guarantee correct and reliable behavior.

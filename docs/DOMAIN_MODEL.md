# Domain Model

This document describes the **domain model of the Smart Spaces project**, including the main entities, their
responsibilities, invariants, and collaborations. The domain model represents the core business concepts and rules,
independent of user interface or infrastructure concerns.

---

## Overview of the Domain

The Smart Spaces domain revolves around three main concepts:

- **Users**, who interact with the system.
- **Spaces**, which represent physical locations that can be reserved.
- **Bookings**, which represent a time-bound reservation of a space by a user.

Each entity encapsulates its own rules and guarantees its own validity.

---

## Entities and Responsibilities

### User

**Responsibility**

- Represent a person registered in the system.
- Provide identity and activity status.
- Serve as the actor that creates bookings.

**Key Attributes**

- `user_id`
- `name`, `surname1`, `surname2`
- `active` state

**Behavior**

- Provide full name.
- Indicate whether the user is active.

---

### Space

**Responsibility**

- Represent a reservable physical space.
- Define capacity and availability.
- Act as the base abstraction for all space types.

**Key Attributes**

- `space_id`
- `space_name`
- `capacity`
- `space_status`
- `space_type`

**Behavior**

- Indicate availability.
- Enforce capacity constraints.
- Provide a textual representation for display.

---

### SpaceMeetingroom (Specialized Space)

**Responsibility**

- Represent a meeting room with additional characteristics.
- Extend the base space with room-specific attributes.

**Additional Attributes**

- `room_number`
- `floor`
- `num_power_outlets`
- `equipment_list`

**Behavior**

- Validate meeting-room-specific constraints.
- Manage equipment list safely.
- Override space type information.

---

### Booking

**Responsibility**

- Represent a reservation of a space by a user for a time interval.
- Control booking lifecycle and state transitions.

**Key Attributes**

- `booking_id`
- `user`
- `space`
- `start_time`
- `end_time`
- `booking_status`

**Behavior**

- Activate, cancel, and finish bookings.
- Enforce time validity.
- Control state transitions.

---

## Invariants

Invariants are conditions that **must always be true**, both before and after any operation.

### User Invariants

- `user_id` must not be empty.
- A user is either active or inactive, never both.
- Only active users can participate in bookings.

---

### Space Invariants

- `capacity` must be greater than zero.
- `space_id` and `space_name` must not be empty.
- A space always has a valid status.
- A space type must always be defined.

---

### Meeting Room Invariants

- `room_number` must be defined.
- `floor` must be a valid integer.
- `num_power_outlets` must be zero or greater.
- Equipment list must always be a list of strings.

---

### Booking Invariants

- `start_time` must be strictly before `end_time`.
- A booking must always reference a valid user and space.
- Booking status must be one of the defined states.
- A finished or canceled booking cannot return to active state.

---

## Collaborations Between Entities

### User ↔ Booking

- A user creates one or more bookings.
- A booking cannot exist without a user.
- User activity status affects booking creation.

---

### Space ↔ Booking

- A space can have multiple bookings over time.
- A space cannot have overlapping active bookings.
- Booking lifecycle changes space availability.

---

### Space ↔ SpaceMeetingroom

- `SpaceMeetingroom` inherits from `Space`.
- Common behavior is reused via inheritance.
- Specialized behavior is added without affecting base space logic.

---

### Booking ↔ BookingService (Contract Interaction)

- Booking creation and lifecycle transitions are coordinated by the application service.
- The domain enforces rules, while the service orchestrates interactions.

---

## Domain Boundaries

- The domain layer does **not** depend on infrastructure or presentation layers.
- All critical business rules are enforced within domain entities.
- External systems interact with the domain only through defined contracts.

---

## Summary

The Smart Spaces domain model:

- Clearly separates responsibilities across entities.
- Uses inheritance to model specialization.
- Enforces invariants to ensure system consistency.
- Defines explicit collaborations between users, spaces, and bookings.

This model forms the foundation upon which the rest of the system is built.

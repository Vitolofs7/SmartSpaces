# Description and Scope

## Functional Description

This project provides an **Intelligent Space Management System** designed to help organizations manage and coordinate
the use of shared physical spaces such as meeting rooms, classrooms, offices, and work areas.

From the user's perspective, the system allows:

- Viewing the list of available spaces and their characteristics.
- Checking whether a space is available for a specific period of time.
- Making reservations for spaces according to predefined rules.
- Cancelling or finishing existing bookings.
- Managing users with different permissions and usage limits.

The system is operated through a **console-based menu**, where users select actions by choosing numbered options. All
interactions are guided and validated by the system, ensuring that invalid operations (such as double bookings or
exceeding user limits) are automatically prevented.

Different types of users have different capabilities. For example, some users may have stricter limits on booking
duration or number of active reservations, while others may enjoy more flexibility. Similarly, different types of spaces
may impose specific conditions or offer additional features.

The goal for the user is to **efficiently reserve and manage shared spaces** without conflicts, while relying on the
system to enforce rules and maintain consistency.

---

## Phase Objectives

The objectives of the current phase of the project are:

- To provide a **functional implementation** of a space reservation system backed by a relational database.
- To allow users to interact with the system using a clear and structured menu.
- To ensure that booking rules are applied automatically and consistently.
- To validate the logical behavior of users, spaces, and bookings under different scenarios.
- To persist all data in a **SQLite database** (`smartspaces.db`) so that state survives between executions.
- To serve as a foundation for future extensions or improvements.

This phase focuses on correctness, clarity of behavior, completeness of the core functionality, and durable data
persistence through a relational database.

---

## Project Scope

### Included Functionality

The scope of this project includes:

- Management of users with different roles and usage rules.
- Management of multiple types of spaces with shared and specific attributes.
- Creation, cancellation, and completion of space bookings.
- Automatic validation of:
    - Space availability.
    - Booking overlaps.
    - User-specific limits and permissions.
    - Space-specific constraints.
- Listing and querying users, spaces, and bookings.
- Clear feedback to the user when an operation is not allowed.
- Persistent storage of all data in a **SQLite relational database**.
- Database initialization and seeding via the `crear_bd.py` script.

---

### Excluded Functionality

The following aspects are explicitly out of scope:

- Graphical user interfaces (GUI) or web-based interfaces.
- Authentication mechanisms (passwords, login systems).
- Integration with external services such as calendars, notifications, or sensors.
- Payment processing or billing features.
- Real-time or concurrent multi-user access.

---

### Assumptions

The project assumes that:

- The system is used by a **single operator at a time** via the console.
- Users interact with the system in good faith (no malicious input).
- The database file (`smartspaces.db`) exists and has been initialized via `crear_bd.py` before running the application.
- The set of users and spaces is relatively small and manageable.

---

### Limits and Constraints

- The system is not optimized for large-scale usage.
- Error handling is focused on logical consistency rather than exhaustive input sanitization.
- The application is intended for **educational and demonstrative purposes**, not for production use.
- Concurrent access to the database from multiple processes is not supported.

---

## Summary

This project delivers a clear and structured implementation of a shared space management system, emphasizing correct
behavior, rule enforcement, user-oriented interaction, and durable data persistence via SQLite. It establishes a solid
base for understanding and extending space reservation logic in future phases.
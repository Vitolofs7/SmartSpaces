# Description and Scope

## Functional Description

This project provides an **Intelligent Space Management System** designed to help organizations manage and coordinate
the use of shared physical spaces such as meeting rooms, classrooms, offices, and work areas.

From the user’s perspective, the system allows:

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

- To provide a **functional simulation** of a space reservation system.
- To allow users to interact with the system using a clear and structured menu.
- To ensure that booking rules are applied automatically and consistently.
- To validate the logical behavior of users, spaces, and bookings under different scenarios.
- To serve as a foundation for future extensions or improvements.

This phase focuses on correctness, clarity of behavior, and completeness of the core functionality rather than
performance, persistence, or user interface design.

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

All data is managed **in memory** during execution.

---

### Excluded Functionality

The following aspects are explicitly out of scope:

- Graphical user interfaces (GUI) or web-based interfaces.
- Persistent storage (databases or file-based saving).
- Authentication mechanisms (passwords, login systems).
- Integration with external services such as calendars, notifications, or sensors.
- Payment processing or billing features.
- Real-time or concurrent multi-user access.

---

### Assumptions

The project assumes that:

- The system is used by a **single operator at a time** via the console.
- Users interact with the system in good faith (no malicious input).
- All data is temporary and only relevant during a single execution.
- The set of users and spaces is relatively small and manageable.

---

### Limits and Constraints

- All information is lost when the program terminates.
- The system is not optimized for large-scale usage.
- Error handling is focused on logical consistency rather than exhaustive input sanitization.
- The application is intended for **educational and demonstrative purposes**, not for production use.

---

## Summary

This project delivers a clear and structured simulation of a shared space management system, emphasizing correct
behavior, rule enforcement, and user-oriented interaction. It establishes a solid base for understanding and extending
space reservation logic in future phases.

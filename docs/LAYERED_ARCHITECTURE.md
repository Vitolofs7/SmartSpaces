# Layered Architecture

## Architectural Overview

The Smart Spaces project follows a **layered architecture**, designed to clearly separate responsibilities, improve
maintainability, and support future evolution of the system.

The architecture is organized into the following layers:

presentation → application → domain
↑
infrastructure

Each layer has a well-defined role, and **dependencies are strictly controlled** to avoid coupling and preserve the
integrity of the domain model.

---

## Domain Layer

### Responsibility

The **domain layer** contains the **core business logic** of the system. It represents the problem space and defines:

- Core entities such as users, spaces, and bookings
- Business rules and validations
- Domain behaviors and invariants
- Relationships between domain objects

This layer is completely independent of technical concerns such as storage, user interfaces, or frameworks.

### Key Characteristics

- No dependency on any other layer
- Contains pure business logic
- Uses object-oriented principles such as:
    - Encapsulation
    - Inheritance
    - Polymorphism
    - Multiple inheritance where appropriate

### Examples

- `User` and specialized user types
- `Space` and subclasses like meeting rooms
- `Booking` and booking status rules

---

## Application Layer

### Responsibility

The **application layer** coordinates use cases and orchestrates interactions between the domain and external systems.

It is responsible for:

- Implementing application use cases (e.g. create booking, cancel booking)
- Enforcing application-level rules
- Managing workflows involving multiple domain objects
- Acting as a boundary between the domain and the outside world

This layer does **not** contain business rules themselves, but rather ensures that domain rules are applied correctly.

### Dependencies

- Depends on the **domain layer**
- Interacts with repositories through abstractions
- Does not depend on infrastructure implementations

### Examples

- `BookingService`
- Use case logic for listing, creating, canceling, and finishing bookings

---

## Presentation Layer

### Responsibility

The **presentation layer** handles all interaction with the user.

In this project, it is implemented as a **command-line interface (CLI)** and is responsible for:

- Displaying menus and information
- Reading user input
- Formatting output for readability
- Translating user actions into application use case calls

This layer contains no business logic and does not manipulate domain objects directly.

### Dependencies

- Depends only on the **application layer**
- Never accesses the domain layer directly
- Never accesses infrastructure directly

### Examples

- `menu.py`
- Input validation and output formatting

---

## Infrastructure Layer

### Responsibility

The **infrastructure layer** provides technical implementations required by the application layer, acting as an *
*adapter** to external systems.

In this project, infrastructure concerns include:

- In-memory repositories
- Seed data initialization
- Persistence abstractions (without real databases)

### Key Characteristics

- Implements interfaces expected by the application layer
- Depends on the **domain layer**
- Can be replaced without affecting application or domain logic

### Dependencies

- May depend on the domain layer
- Is used by the application layer via abstractions
- Is never accessed directly by the presentation layer

### Examples

- `SpaceMemoryRepository`
- `UserMemoryRepository`
- `BookingMemoryRepository`
- `seed_data`

---

## Dependency Rules

The following dependency rules are enforced:

- **Presentation → Application**
- **Application → Domain**
- **Infrastructure → Domain**
- **Application → Infrastructure (via abstractions only)**

The following dependencies are **not allowed**:

- Domain depending on any other layer
- Application depending on presentation
- Presentation depending on domain or infrastructure
- Infrastructure depending on presentation or application logic

---

## Benefits of This Architecture

- Clear separation of concerns
- High maintainability and readability
- Easy testing of domain and application logic
- Infrastructure can be replaced or extended with minimal impact
- Domain model remains clean and independent

---

## Summary

The layered architecture used in Smart Spaces ensures that business logic remains central and protected, while technical
and interaction concerns are isolated in their respective layers. This structure supports scalability, clarity, and
long-term evolution of the system.
# Repository Contract

This document describes the **repository contract used in the Smart Spaces project**, defining the expected behavior of
repositories, the operations they must support, and how they can be replaced with alternative persistence mechanisms.

---

## Purpose of the Repository Contract

Repositories act as an **abstraction layer between the domain/application logic and the persistence mechanism**. Their
goal is to:

- Isolate business logic from storage details.
- Allow easy replacement of in-memory storage with other persistence solutions.
- Provide a consistent interface for accessing domain entities.

The application layer depends only on the repository contract, never on a concrete implementation.

---

## Repositories in the Project

The project defines repositories for the main domain entities:

- `SpaceRepository`
- `UserRepository`
- `BookingRepository`

In the current implementation, all repositories are **in-memory repositories**, but the contract allows other
implementations (database, files, APIs, etc.).

---

## Expected Repository Operations

Each repository must support the following operations.

### Save

**Responsibility**

- Store a new entity or update an existing one.

**Behavior**

- If an entity with the same identifier already exists, it is replaced.
- The operation must not alter the entity state.

**Example**

- Save a new space.
- Update a booking after changing its status.

---

### Get (by ID)

**Responsibility**

- Retrieve a single entity by its unique identifier.

**Behavior**

- Returns the entity if found.
- Raises an error if the entity does not exist.

**Example**

- Retrieve a user by `user_id`.
- Retrieve a booking by `booking_id`.

---

### List (All)

**Responsibility**

- Retrieve all stored entities of a given type.

**Behavior**

- Returns a collection of entities.
- Order is not guaranteed unless explicitly defined.

**Example**

- List all spaces.
- List all bookings.

---

### Delete (In-Memory Only)

**Responsibility**

- Remove an entity from storage.

**Behavior**

- Used only in in-memory implementations.
- Typically for testing or temporary data handling.
- Not required for all persistence mechanisms.

---

## Repository Contract Summary

| Operation           | Description                  |
|---------------------|------------------------------|
| `save(entity)`      | Stores or updates an entity  |
| `get(entity_id)`    | Retrieves an entity by ID    |
| `list()`            | Returns all entities         |
| `delete(entity_id)` | Removes an entity (optional) |

---

## Current In-Memory Implementation

The current repositories (`SpaceMemoryRepository`, `UserMemoryRepository`, `BookingMemoryRepository`) implement the
contract using:

- Internal collections (lists or dictionaries).
- Simple lookup by ID.
- No persistence beyond application runtime.

These implementations are suitable for:

- Prototyping.
- Educational purposes.
- Unit testing.

---

## Replacing the Persistence Mechanism

One of the main benefits of using repository contracts is the ability to **replace storage without modifying business
logic**.

### Example: Database Persistence

To replace the in-memory repository with a database-backed repository:

1. Create a new repository class (e.g. `SpaceDatabaseRepository`).
2. Implement the same methods (`save`, `get`, `list`, `delete` if applicable).
3. Internally map entities to database records.
4. Inject the new repository into the application service.

No changes are required in:

- Domain entities.
- Application services.
- Presentation layer.

---

### Example: File-Based Persistence

Similarly, repositories could be implemented using:

- JSON files.
- CSV files.
- Serialized objects.

As long as the repository respects the contract, the rest of the system remains unaffected.

---

## Dependency Direction

- **Application layer depends on repository interfaces/contracts.**
- **Infrastructure layer provides concrete implementations.**
- **Repositories never depend on presentation logic.**

This guarantees a clean separation of concerns and aligns with the layered architecture of the project.

---

## Summary

The repository contract in Smart Spaces:

- Defines a clear and minimal interface for persistence.
- Enables easy substitution of storage mechanisms.
- Protects domain and application layers from infrastructure changes.
- Supports scalability and maintainability of the system.

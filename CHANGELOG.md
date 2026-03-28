# Changelog

## All relevant project changes, organized by version/release.

---

## [0.4.1] - 2026-03-28

### Fixed (Bug Fixes)

- Fixed `UNIQUE constraint failed: spaces.space_id` error triggered when creating a booking,
  caused by `BookingService` incorrectly persisting the associated `Space` object.
  Space persistence is now handled exclusively by `SpaceRepository`.
- Fixed `create_booking()` returning `None` due to incorrect control flow in the creation pipeline;
  the method now always returns a valid `Booking` instance.
- Fixed `booking_id` being `None` at persistence time; automatic ID generation (`B1`, `B2`, `B3`, …)
  is now handled by `BookingSQLiteRepository`, querying the database to avoid collisions with existing IDs.
- Fixed `UNIQUE constraint failed: bookings.booking_id` caused by dual persistence:
  both `Booking.create()` and `BookingService` were saving the booking independently.
  Removed the redundant save to ensure a single persistence point.
- Fixed `BookingSQLiteRepository.list()` being called with arguments (`user_repo`, `space_repo`);
  the method takes no parameters and resolves its dependencies internally.
- Fixed space ID differentiation between `Space` and `SpaceMeetingRoom`:
  generic spaces now use the `S1, S2, S3…` series and meeting rooms use `SM1, SM2, SM3…`.
- Fixed `SpaceSQLiteRepository` generating `None` IDs due to incorrect access to `_space_id`
  and counters not being initialised from the database; corrected attribute access and
  synchronised counters against existing rows on startup.
- Fixed ID counter collision caused by mixed prefix handling (`S` and `SM`);
  counters are now computed with separate queries:
  `LIKE 'S%' AND NOT LIKE 'SM%'` for generic spaces and `LIKE 'SM%'` for meeting rooms.
- Fixed database seed script (`crear_bd.py`) using `S`-prefixed IDs for `SpaceMeetingRoom` rows;
  seed data now uses `SM1`, `SM2`, … and booking foreign keys updated accordingly.
- Fixed `AttributeError: _last_meeting_id` in `SpaceSQLiteRepository` by adding the missing
  instance counters `_last_generic_id` and `_last_meeting_id`.
- Fixed `meeting_rooms` insert failing when `equipment_list` was `None`;
  the value is now normalised to an empty string before persistence.

---

## [0.4.0] - 2026-03-21

### Added (New Features)

- Added `crear_bd.py` script at the project root to initialize the SQLite database (`smartspaces.db`) from scratch.
- Created four relational tables in SQLite:
  - `spaces`: stores common attributes for all space types (`space_id`, `space_name`, `capacity`, `space_type`, `space_status`).
  - `meeting_rooms`: stores `SpaceMeetingRoom`-specific attributes (`room_number`, `floor`, `equipment_list`, `num_power_outlets`) with a FOREIGN KEY referencing `spaces`.
  - `users`: stores user data including `active` status as INTEGER (1=active, 0=inactive).
  - `bookings`: stores booking records with FOREIGN KEYs referencing both `spaces` and `users`; datetimes stored as ISO 8601 TEXT.
- `crear_bd.py` seeds all tables with the same initial data previously defined in `infrastructure/seed_data.py`.
- `crear_bd.py` automatically drops and recreates the database on each run to ensure a clean state.
- `crear_bd.py` prints a verification summary of all four tables after insertion.
- Updated `docs/README.md` to include `python crear_bd.py` as step 3 in the Quick Start section.
- Updated `docs/LAYERED_ARCHITECTURE.md` to document the database schema table and describe the infrastructure layer as SQLite-backed.
- Updated `docs/BUSINESS_RULES.md` to include a **Database Integrity Rules** section covering FOREIGN KEY enforcement, NOT NULL constraints, and `PRAGMA foreign_keys = ON`.
- Updated `docs/DOMAIN_MODEL.md` to include database mapping for each entity (`spaces`, `meeting_rooms`, `users`, `bookings` tables).
- Updated `docs/INITIAL_DATA.md` to reference `crear_bd.py` instead of `seed_data.py` and document SQL-based data modification.
- Updated `docs/EXECUTION.md` to add a **Setting Up the Database** section with commands to initialize, reset, and delete the database.
- Updated `docs/DESCRIPTION_AND_SCOPE.md` to reflect SQLite persistence as an included feature and remove persistent storage from excluded functionality.

### Changed (Changes)

- Mapped `SpaceMeetingRoom` inheritance to two related tables (`spaces` + `meeting_rooms`) following the joined-table inheritance pattern.
- `equipment_list` stored as a comma-separated TEXT string in the `meeting_rooms` table (use `.split(",")` to recover the list in Python).
- Space status updated to `RESERVED` in the `spaces` table for spaces with active bookings at seed time.
- Updated `README.md` to reflect SQLite-backed persistence: revised Overview, Architecture, Installation, and Project Structure sections; added **Database Management** section with commands to create, reset, and delete the database.

### Fixed (Bug Fixes)

- None.

### Deprecated (Deprecated)

- `infrastructure/seed_data.py` in-memory seeding is superseded by `crear_bd.py` for database-backed persistence.

### Removed (Removed)

- Removed **Persistent storage** from the excluded functionality section in `docs/DESCRIPTION_AND_SCOPE.md`.

### Security (Security)

- All SQL inserts use parameterized queries (`?` placeholders) to prevent SQL injection.
- `PRAGMA foreign_keys = ON` enabled to enforce referential integrity across all tables.

### Compatibility / Breaking Changes (Compatibility)

- `python crear_bd.py` must be executed before launching the application for the first time.
- In-memory repositories remain active and are still used by the test suite; no changes to existing tests.

---

## [0.3.5] - 2026-03-05

### Added (New Features)

- Added `docs/README.md` as an index and entry point for the `docs/` folder, listing all documents with descriptions and
  a Quick Start section.

### Changed (Changes)

- Updated `docs/EXECUTION.md` to cover phase 03:
  - Added **Running Tests** section with commands to run the full test suite via `unittest discover`.
  - Added **Running Tests with Coverage** subsection with the complete four-step sequence:
    `pip install -r requirements.txt`, `coverage run`, `coverage report`, and optional `coverage html`.
- Updated `docs/TESTS_AND_STEPS.md`:
  - Added subsection **4.1 How to Reproduce Coverage Results** under the Test Coverage section, documenting the full
    command sequence to reproduce the reported coverage percentages.
- Renamed `SpaceMeetingroom` to `SpaceMeetingRoom` across `domain/space_meetingroom.py` to follow Python naming
  conventions (`Room` as an independent word).
- Renamed setter parameters `v` to their descriptive names (`room_number`, `floor`, `num_power_outlets`) in
  `domain/space_meetingroom.py`.
- Renamed parameter `n` to `num_people` in `can_accommodate` method (`domain/space_meetingroom.py`).
- Renamed local variable `eq` to `equipment_display` in `__str__` (`domain/space_meetingroom.py`).
- Renamed `_data` attribute to `_bookings`, `_spaces`, and `_users` in the three memory repositories for clarity.
- Renamed single-letter variables `b`, `u`, `s` to `booking`, `user`, `space` in `application/booking_service.py` and
  `presentation/menu.py`.
- Standardized repository attribute naming across services: `_booking_repo`, `_space_repo`, and `_user_repo` (replacing
  `_user_repository` in `UserService`).
- Removed obvious inline comments in `presentation/menu.py` (lines 136–176) that restated what the code already
  expressed.
- Fixed typo in `docs/BUSINESS_RULES.md`: replaced `CANCELED` with `CANCELLED` to match the codebase.
- Removed undocumented user role descriptions (`Basic Users`, `Premium Users`, `Administrators`) from `README.md` (lines
  64–77) as they do not correspond to any implemented class; updated the section to describe the actual `User` domain
  class.
- Injected `booking_repo` into `SpaceService.__init__` and removed it as a parameter from `get_available_spaces`, so
  the presentation layer no longer handles repositories directly.
- Updated `BookingService.create_booking` to enforce user-level booking constraints defined in the domain: maximum
  number of concurrent active bookings (`max_active_bookings`) and maximum booking duration (`max_booking_duration`).
- Reworked availability logic in `Booking.create`: availability is now determined exclusively by the absence of
  overlapping active bookings. `MAINTENANCE` remains a global block, but `RESERVED` status no longer prevents future
  non-overlapping bookings for the same space.
- Removed `_check_overlap` from `BookingService`: overlap validation is now delegated entirely to the domain layer
  (`Booking.create`), eliminating the duplication between service and domain.
- Removed `space_id` parameter from `SpaceService.create_space` and `create_meeting_room`: space IDs are now assigned
  automatically by `SpaceMemoryRepository`, consistent with the existing behavior for bookings.
- Updated `presentation/menu.py` option 7 to no longer prompt the operator for a Space ID.
- Updated `domain/space.py` constructor to accept `space_id=None` to support auto-ID assignment by the repository.
- Updated `domain/space.py` `reserve()` method: removed the `AVAILABLE`-only guard; the method now only blocks if the
  space is under `MAINTENANCE`, allowing a `RESERVED` space to accept additional non-overlapping bookings.
- Added `is_maintenance()` method to `domain/space.py` to support the maintenance check in `Booking.create`.
- Added auto-increment ID generation to `SpaceMemoryRepository`, consistent with `BookingMemoryRepository`.

### Fixed (Bug Fixes)

- Removed unused class attribute `_id_counter = 1` from `domain/booking.py`.
- Removed unused instance attribute `self._bookings = {}` from `domain/space.py`.
- Fixed `cancel_booking` and `finish_booking` in `BookingService`: removed redundant `space.release()` and
  `space_repo.save()` calls that caused `ValueError: Space not reserved` because the domain methods `booking.cancel()`
  and `booking.finish()` already handle the space state transition internally.
- Fixed `ValueError: Space not available` when booking a `RESERVED` space for a non-overlapping time range, caused by
  `reserve()` rejecting any space not in `AVAILABLE` status.
- Fixed `AttributeError: 'Space' object has no attribute 'is_maintenance'` raised during booking creation after
  `Booking.create` was updated to check for maintenance status.

### Deprecated (Deprecated)

- None.

### Removed (Removed)

- None.

### Security (Security)

- None.

### Compatibility / Breaking Changes (Compatibility)

- **Breaking**: `SpaceMeetingroom` renamed to `SpaceMeetingRoom`. Update any imports or references across the codebase.
- **Breaking**: `SpaceService.__init__` now requires `booking_repo` as a second argument. Update all instantiation sites
  accordingly.
- **Breaking**: `SpaceService.get_available_spaces` signature changed from `(booking_repo, start, end)` to
  `(start, end)`. Update any call sites in the presentation layer.
- **Breaking**: `SpaceService.create_space` signature changed from `(space_id, space_name, capacity, space_type)` to
  `(space_name, capacity, space_type)`. Update any call sites accordingly.
- **Breaking**: `SpaceService.create_meeting_room` signature changed from `(space_id, space_name, ...)` to
  `(space_name, ...)`. Update any call sites accordingly.
- **Breaking**: `domain/space.py` constructor now accepts `space_id=None`; existing code passing empty strings as IDs
  will no longer raise `ValueError` — pass `None` explicitly for auto-assignment.
- All other changes are backward-compatible.

---

## [0.3.4] - 2026-02-11

### Added (New Features)

- Implemented comprehensive **unit tests** for domain classes:
  - `Booking` domain:
    - Full coverage for creation, cancellation, finishing, overlap detection, and rescheduling.
    - Tests for invalid users, unavailable spaces, and overlapping bookings.
  - `Space` domain:
    - Tests for creation, invalid values, status transitions (`AVAILABLE`, `RESERVED`, `MAINTENANCE`), and helper
      methods (`is_available`, `is_reserved`, `reserve`, `release`).
  - `User` domain:
    - Tests for creation, invalid fields, deactivation, full name property, and booking permissions.
- Added **integration tests** (`TestIntegrationBookingSystem`) to simulate full booking flows including:
  - Multiple users and spaces.
  - Booking creation, cancellation, finishing, and rescheduling.
  - Validation for inactive users and spaces in maintenance.
  - Verification of booking IDs uniqueness.

### Changed (Changes)

- Refactored **integration test `test_full_booking_flow`**:
  - Ensured `finish()` only called on active reservations to prevent `Space not reserved` errors.
  - Adjusted test steps to properly handle spaces before and after maintenance mode.
  - Rearranged booking/cancellation flow to prevent invalid state transitions during testing.
- Updated test mocks for repository behavior:
  - `FakeBookingRepo` now assigns `_booking_id` automatically.
  - Ensures `Booking.create` interacts with the repo similarly to real application behavior.
- Updated unit tests to increase code coverage:
  - `Booking` coverage now 93–100% including edge cases.
  - `Space` coverage improved to 97–100%.
  - `User` coverage improved to 97–100%.

### Fixed (Bug Fixes)

- Resolved `ValueError: Space not reserved` in integration test by correcting the order of operations for finishing and
  maintenance transitions.
- Fixed minor edge-case errors in unit tests:
  - Overlapping bookings detection.
  - Rescheduling with active and inactive bookings.
  - Creation of bookings on unavailable or maintenance spaces.

### Deprecated (Deprecated)

- None.

### Removed (Removed)

- None.

### Security (Security)

- None.

### Compatibility / Breaking Changes (Compatibility)

- Fully backward-compatible with domain and service layers.
- No changes to production code logic; only tests were added and integration flow corrected.

---

## [0.3.3] - 2026-02-04

### Added (New Features)

- Added **option 8: List available spaces** with date range filtering.
- Added **option 9: Modify booking** to reschedule existing bookings.
- Implemented `BookingService.modify_booking(booking_id, new_start, new_end)` in the application layer.
- Added `get_available_spaces` method in `SpaceService` to return spaces free in a given datetime range.
- Seed data updated to include sample bookings for testing availability logic.

### Changed (Changes)

- Updated `menu.py` to integrate date-based filtering and modification of bookings.
- Refactored booking creation to use standardized date input format (`YYYY-MM-DD HH:MM` or `YYYY/MM/DD HH:MM`).
- Improved display of bookings and spaces in the console for clarity.

### Fixed (Bug Fixes)

- Corrected filtering of spaces when checking availability for a given date range.
- Fixed minor inconsistencies in booking status display.

### Deprecated (Deprecated)

- None.

### Removed (Removed)

- None.

### Security (Security)

- Centralized validation for booking modification to prevent invalid states.

### Compatibility / Breaking Changes (Compatibility)

- **Breaking**: Menu options shifted (previous option 8 → now 8/9 for new features). Update any scripts calling menu
  options.
- `BookingService.modify_booking` enforces overlap and user/space validation.

---

## [0.3.2] - 2026-02-04

### Added (New Features)

- **List available spaces by date range**:
  - Added option **8. List available spaces** in the console menu.
  - Users can enter a start and end datetime.
  - System lists only spaces that are not booked in that range.
- Enhanced **date input parsing** for bookings with flexible formats (`YYYY-MM-DD HH:MM` and `YYYY/MM/DD HH:MM`).
- Updated seed data to include **sample bookings** for testing.

### Changed (Changes)

- Refactored presentation layer (`menu.py`) to support date input for available spaces.
- `BookingService` used to check active bookings when listing availability.

### Fixed (Bug Fixes)

- Validations prevent showing already reserved spaces for the selected period.
- Corrected date format handling in presentation layer.

### Compatibility / Breaking Changes (Compatibility)

- **Breaking**: Menu now includes option 8; numbering shifted for subsequent options.
- Spaces marked as reserved are considered unavailable in the date range query.

---

## [0.3.1] - 2026-02-04

### Added (New Features)

- Refactored all in-memory repositories (`BookingMemoryRepository`, `SpaceMemoryRepository`, `UserMemoryRepository`) to
  use automatic ID generation (for bookings) and simplified one-line methods.
- Services (`BookingService`, `SpaceService`, `UserService`) refactored for compactness while maintaining all business
  logic and functionality.
- Internal helpers in services remain but code footprint minimized for readability and maintainability.

### Changed (Changes)

- Compact code format applied to:
  - `application/booking_service.py`
  - `application/space_service.py`
  - `application/user_service.py`
  - `infrastructure/booking_memory_repository.py`
  - `infrastructure/space_memory_repository.py`
  - `infrastructure/user_memory_repository.py`
- Removed redundant docstrings in repository implementations (interfaces remain documented).

### Fixed (Bug Fixes)

- No functional changes; all behaviour preserved.

### Deprecated (Deprecated)

- No deprecated features in this release.

### Removed (Removed)

- Removed multi-line repetitive docstrings and comments in repository classes to streamline code.

### Security (Security)

- No security changes.

### Compatibility / Breaking Changes (Compatibility)

- Fully backward-compatible: all public methods and interfaces remain unchanged.

---

## [0.3.0] - 2026-02-04

### Added (New Features)

- Automatic ID generation for `Booking` in `BookingMemoryRepository`.
- Service-layer orchestration for all operations: `BookingService`, `SpaceService`, `UserService`.
- All presentation interactions now go through application services instead of accessing repositories directly.
- Validation in services and domain for booking overlaps, space availability, and user activity.
- Updated `Space` and `SpaceMeetingroom` to fully encapsulate state changes (`reserve`, `release`, `maintenance`) and
  validation logic.
- `User` entity enforces required fields and supports `full_name()`, `is_active()`, and booking-related rules.

### Changed (Changes)

- Refactored `Booking` domain class:
  - Removed manual ID generation from presentation and service layers.
  - Factory method `Booking.create` now uses repository for storage and ID assignment.
  - Domain encapsulates booking logic: activation, cancellation, finishing, and overlap checks.
- Refactored `Space` domain class to:
  - Manage status internally (`AVAILABLE`, `RESERVED`, `MAINTENANCE`).
  - Provide helper methods for reservations and releases.
- Refactored `User` domain class to:
  - Include active status and booking rules.
  - Expose `full_name()` and `can_make_booking()` for service layer use.
- Menu (`presentation/menu.py`) now delegates all data operations to services and passes only user-friendly
  identifiers (names) instead of IDs.

### Fixed (Bug Fixes)

- Fixed circular import issues between `Booking` and `BookingRepository`.
- Fixed previous bug where `booking_id` was incorrectly passed or generated in the service/presentation layer.
- Fixed overlapping booking validation and automatic reservation of spaces in domain layer.
- Corrected service logic to properly delegate domain responsibilities and avoid direct repository manipulation.

### Deprecated (Deprecated)

- Manual ID assignment in presentation and service layers for `Booking`.
- Direct repository access from the menu for listing entities.

### Removed (Removed)

- Removed creation of domain objects in the menu (`presentation`) layer.
- Removed all direct manipulation of domain attributes from upper layers.

---

## [0.2.0] - 2026-01-31

### Added (New Features)

- Added the `SpaceMeetingroom` subclass as a specialization of `Space`.
- Incorporated the `space_type` attribute with overriding in child classes.
- Added option **7. Create space** to the console menu.
- Support for dynamic creation of generic spaces and meeting rooms from the menu.
- Detailed visualization of spaces, displaying specific attributes of `MeetingRoom`.
- Implemented `__str__` methods to improve information presentation in the console.
- Added complete documentation in the `docs/` folder:
  - `DESCRIPTION_AND_SCOPE.md`
  - `EXECUTION.md`
  - `LAYERED_ARCHITECTURE.md`
  - `USE_CASES.md`
  - `BUSINESS_RULES.md`
  - `DOMAIN_MODEL.md`
  - `REPOSITORY_CONTRACT.md`
- Added this `CHANGELOG.md` file to track project evolution.

### Changed (Changes)

- Updated `README.md` to include:
  - General project description.
  - Objectives.
  - Requirements.
  - Installation and execution instructions.
- Refactored the menu (`presentation/menu.py`) to:
  - Centralize date validations.
  - Delegate business logic to `BookingService`.
  - Improve readability and user flow structure.
- Adjusted the space repository to store instances of `SpaceMeetingroom` subclasses.

### Fixed (Bug Fixes)

- Fixed space visualization to avoid accessing non-existent attributes.
- Fixed validation errors when creating spaces from the menu.
- Avoided direct use of private attributes in the presentation layer when possible.

### Deprecated (Deprecated)

- Direct use of data structures without repositories (manual lists) in upper layers.

### Removed (Removed)

- Removed space creation logic directly in the domain without validation.
- Removed unclear prints in menu output.

### Security (Security)

- Avoided exposing sensitive internal domain states directly in the console.
- Centralized validations to prevent inconsistent states.

### Compatibility / Breaking Changes (Compatibility)

- **Breaking**: `Space` now requires the `space_type` attribute.
- **Breaking**: the menu depends on spaces correctly implementing `__str__`.
- To migrate:
  - Update any `Space` creation to include `space_type`.
  - Ensure new subclasses correctly override the space type.

---

## [0.1.0] - 2026-01-14

### Added (New Features)

- Initial version of the Smart Spaces system.
- Console menu with basic management of:
  - Spaces.
  - Users.
  - Bookings.
- Layered implementation:
  - `presentation`
  - `application`
  - `domain`
  - `infrastructure`
- In-memory repositories for spaces, users, and bookings.
- Application service `BookingService`.
- Sample data loaded at application startup.

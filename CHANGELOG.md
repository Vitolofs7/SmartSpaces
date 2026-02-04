# Changelog

All relevant project changes, organized by version/release.
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

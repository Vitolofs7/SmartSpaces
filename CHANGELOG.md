# Changelog

All relevant project changes, organized by version/release.
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

---

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

---

### Fixed (Bug Fixes)

- Fixed space visualization to avoid accessing non-existent attributes.
- Fixed validation errors when creating spaces from the menu.
- Avoided direct use of private attributes in the presentation layer when possible.

---

### Deprecated (Deprecated)

- Direct use of data structures without repositories (manual lists) in upper layers.

---

### Removed (Removed)

- Removed space creation logic directly in the domain without validation.
- Removed unclear prints in menu output.

---

### Security (Security)

- Avoided exposing sensitive internal domain states directly in the console.
- Centralized validations to prevent inconsistent states.

---

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

---
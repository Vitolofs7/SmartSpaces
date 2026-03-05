# Smart Spaces — Documentation Index

This folder contains the technical and functional documentation for the **Smart Spaces** project. Each document covers a specific aspect of the system design, behavior, or operation.

---

## Documents

### [`DESCRIPTION_AND_SCOPE.md`](./DESCRIPTION_AND_SCOPE.md)
Functional description of the system, phase objectives, included and excluded functionality, assumptions, and constraints. Start here for a high-level understanding of what the project does and why.

---

### [`DOMAIN_MODEL.md`](./DOMAIN_MODEL.md)
Description of the core domain entities (`User`, `Space`, `SpaceMeetingroom`, `Booking`), their responsibilities, invariants, and collaborations. Explains the business concepts independently of any technical implementation.

---

### [`LAYERED_ARCHITECTURE.md`](./LAYERED_ARCHITECTURE.md)
Overview of the four-layer architecture (domain, application, infrastructure, presentation), the responsibilities of each layer, and the dependency rules that keep the system decoupled and maintainable.

---

### [`BUSINESS_RULES.md`](./BUSINESS_RULES.md)
All business rules enforced by the domain layer: space creation and status rules, user constraints, booking lifecycle rules, state transitions, and error handling principles.

---

### [`USE_CASES.md`](./USE_CASES.md)
Functional use cases available through the CLI menu (UC-1 to UC-8). Each use case documents its inputs, validations, expected output, and possible errors from the user's perspective.

---

### [`REPOSITORY_CONTRACT.md`](./REPOSITORY_CONTRACT.md)
Definition of the repository abstraction layer: the operations each repository must support (`save`, `get`, `list`, `delete`), the current in-memory implementation, and how to replace it with a different persistence mechanism.

---

### [`INITIAL_DATA.md`](./INITIAL_DATA.md)
Description of the seed data provided by `infrastructure/seed_data.py`: the preloaded spaces, users, and bookings, and how to modify or extend them for testing or demo purposes.

---

### [`EXECUTION.md`](./EXECUTION.md)
Step-by-step guide for running the application, including requirements, the command to launch the CLI menu, example interaction flows, and instructions for running tests and generating coverage reports.

---

### [`TESTS_AND_STEPS.md`](./TESTS_AND_STEPS.md)
Detailed description of the test suite: how to run all tests or individual modules, the structure of unit and integration tests, what each test file validates, and the full sequence of commands to reproduce coverage results.

---

## Quick Start

```bash
# 1. (Optional) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
source .venv/Scripts/activate    # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python -m presentation.menu

# 4. Run the tests
python -m unittest discover -s tests -t .

# 5. Check test coverage
coverage run -m unittest discover -s tests -t .
coverage report
```

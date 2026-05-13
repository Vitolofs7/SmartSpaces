<p align="center">
  <img src="./docs/img/app_logo.png" alt="Smart Spaces Logo" width="400"/>
</p>

**Intelligent Space Management System**  
Manage and optimize shared physical spaces such as classrooms, meeting rooms, and workstations, ensuring bookings are conflict-free and usage rules are automatically enforced.

---

Smart Spaces provides a clear, object-oriented simulation of space reservation and user management.  
It focuses on **modular design**, **scalable architecture**, and **rule-enforced bookings** for organizations looking to streamline resource usage.


📖 **Overview**  
The project is an **Intelligent Space Management System** designed to manage and optimize the use of shared physical
spaces within an organization, including classrooms, meeting rooms, workstations, or multipurpose rooms.

The system models reservable spaces, users with different roles, and temporary bookings, while enforcing rules based on
user type, space type, and booking conditions. It emphasizes **object-oriented design**, correct domain logic, and safe
operations without overlapping bookings or unauthorized access.

The focus is on the **domain and business rules**, backed by a **SQLite relational database** for persistent storage.

---

🎯 **Objectives**

**General Objective**  
Develop a modular, object-oriented system that manages shared spaces and bookings coherently, preventing conflicts and
enforcing usage rules.

**Specific Objectives**

- Model users with different roles and booking constraints.
- Represent physical spaces with capacities, status, and additional features.
- Manage bookings ensuring availability and avoiding overlaps.
- Enforce rules depending on user type and space type automatically.
- Leverage inheritance and multiple inheritance for reusable and extensible design.
- Persist all data in a SQLite relational database, replacing in-memory storage.

---

🧩 **Main Domain Entities**

The system revolves around several key entities:

- **User**: Represents people interacting with the system, with different roles and booking limits.
- **Space**: Represents physical resources available for reservation, including generic spaces and specialized meeting
  rooms.
- **Booking**: Links users to spaces for specific time intervals, tracking status and enforcing availability.

---

🏢 **Spaces Management**

The system allows:

- Registering spaces with attributes: ID, name, capacity, type, and status (available, reserved, maintenance).
- Specialized spaces (e.g., meeting rooms) can have additional features such as equipment, floor number, or number of
  power outlets.
- Checking availability for a given time interval and automatically preventing double-booking.

---

👤 **User Management**

User behaviors include:

- Checking active bookings and allowed duration.
- Enforcing booking permissions based on space type.

---

📦 **Bookings and Availability Control**

- Bookings link users and spaces for a defined time period.
- Automatic validations include:
    - Space availability.
    - No overlap with existing bookings.
    - Compliance with user permissions and space rules.
- Booking statuses: **active**, **canceled**, **finished**.
- Bookings can be created, canceled, finished, or rescheduled with conflict detection.

---

🧱 **Architecture**

The system uses a layered architecture:

- **Presentation**: Console-based interactive menu (`presentation.menu`) and Flask REST API (`presentation.app`).
- **Application**: Services coordinating use cases (`BookingService`, `SpaceService`, `UserService`).
- **Domain**: Core models and rules (`User`, `Space`, `Booking`, etc.).
- **Infrastructure**: SQLite-backed repositories and initial seed data.

This separation ensures maintainability, scalability, and clear responsibility for each layer.

---

🚀 **Installation & Execution**

Follow these steps to set up and run the Smart Spaces management system in your local environment.
The repository is on the main branch (`main`) with the current content for delivery.

### **Requirements**

- Python 3.13+
- Flask (`pip install flask`)
- No other external dependencies (SQLite is included in the Python standard library).

### **Installation**

1. Clone the repository:
```bash
  git clone https://github.com/Vitolofs7/SmartSpaces.git
```

2. Go to the root of the project:
```bash
  cd SmartSpaces
```

3. Initialize the database:
```bash
  python create_db.py
```

4. Run the application:
```bash
  python -m presentation.menu
```

### **Database Management**

The database is stored in a single file `smartspaces.db` at the project root.

**Create / recreate the database** (drops existing data and reseeds):
```bash
  python create_db.py
```

**Delete the database manually**:
```bash
  # Linux / Git Bash
  rm smartspaces.db

  # Windows CMD
  del smartspaces.db
```

> ⚠️ Running `create_db.py` again after deletion will recreate the database with the initial seed data.

---

## 🌐 **Web Interface (Flask)**

Smart Spaces also exposes a REST API via Flask, following the **POST-Redirect-GET** pattern for write operations.

### **Starting the server**

Run from the project root:
```bash
python -m presentation.app
```
Then open `http://localhost:5000` in your browser, or interact via `curl`.

---

### 📊 Observability and Logging

The API now includes global observability through logging and help routes:

#### **Log File**

* **Location**: `smartspaces.log` (project root)
* **Content**: Records all HTTP requests, errors, and operations.
* **Format**: `YYYY-MM-DD HH:MM:SS - smartspaces - LEVEL - message`
* **Levels**:

  * `INFO`: Successful operations (creations, updates, access to `/help`)
  * `WARNING`: Resources not found (404), invalid data (400), conflicts (409)
  * `ERROR`: Internal server errors (500)

**Log example:**

```text
2026-05-11 14:32:15 - smartspaces - INFO - GET /users
2026-05-11 14:32:16 - smartspaces - INFO - User created: U99
2026-05-11 14:32:17 - smartspaces - WARNING - User not found: U999
2026-05-11 14:32:18 - smartspaces - INFO - POST /bookings/new/Alice Smith Johnson/Conference Room/2026-05-15T10:00:00/2026-05-15T12:00:00
2026-05-11 14:32:19 - smartspaces - INFO - Booking created: B4
```

#### **`/help` Route**

* **URL**: `http://localhost:5000/help`
* **Content**: HTML table listing all registered routes.
* **Columns**: Route | HTTP Methods | Function (endpoint)
* **Advantage**: Automatically updates whenever routes are added or removed. No manual changes required.

#### **Custom Error Handlers**

* **404 Not Found**: Returns an HTML page with a user-friendly message when accessing a non-existent URL.
* **500 Internal Server Error**: Returns an HTML page if an unhandled error occurs.

#### **Disable or Reconfigure Logging**

If you need to change the logging level or the log file location, edit the beginning of `presentation/app.py`:

```python
logging.basicConfig(
    filename='smartspaces.log',        # ← change log file name or path
    level=logging.INFO,                # ← change to DEBUG, WARNING, ERROR, etc.
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

---

### **Available Routes**

#### 📥 Read (GET)

| Route | Description |
|-------|-------------|
| `GET /` | Welcome page with links to main endpoints |
| `GET /users` | List all users |
| `GET /users/<user_id>` | Get a specific user |
| `GET /spaces` | List all spaces |
| `GET /spaces/<space_id>` | Get a specific space |
| `GET /bookings` | List all bookings |
| `GET /bookings/<booking_id>` | Get a specific booking |
| `GET /spaces/disponibles/<fecha_inicio>/<fecha_fin>` | Available spaces in a date range (ISO 8601) |
| `GET /bookings/usuario/<user_name>` | Bookings for a specific user |
| `GET /bookings/espacio/<space_name>` | Bookings for a specific space |

#### ➕ Create (POST with redirect)

| Route | Description |
|-------|-------------|
| `POST /users/nuevo/<user_id>/<name>/<surname1>/<surname2>` | Create a new user |
| `POST /spaces/nuevo/<space_name>/<int:capacity>/<space_type>` | Create a new space |
| `POST /spaces/nueva-sala/<name>/<capacity>/<room>/<floor>/<outlets>` | Create a meeting room |
| `POST /bookings/nueva/<user>/<space>/<fecha_inicio>/<fecha_fin>` | Create a new booking |

#### 🔄 Status Changes (POST with redirect)

| Route | Description |
|-------|-------------|
| `POST /bookings/<booking_id>/cancelar` | Cancel a booking |
| `POST /bookings/<booking_id>/finalizar` | Mark a booking as finished |
| `POST /bookings/<booking_id>/reprogramar/<nueva_inicio>/<nueva_fin>` | Reschedule a booking |

#### 🚫 Deactivation (POST with redirect)

| Route | Description |
|-------|-------------|
| `POST /users/<user_id>/desactivar` | Deactivate a user |

---

### **HTTP Status Codes**

| Code | Meaning |
|------|---------|
| `200 OK` | Successful operation (GET) |
| `302 Found` | Redirect after POST (POST-Redirect-GET pattern) |
| `400 Bad Request` | Invalid data (malformed date, inactive user, etc.) |
| `404 Not Found` | Resource does not exist |
| `409 Conflict` | Duplicate resource or state conflict |
| `500 Internal Server Error` | Unexpected server error |

---

🌀 **Application Lifecycle & Layered Architecture**  

The Smart Spaces system follows a **layered architecture**, ensuring separation of concerns, maintainability, and clear data flow. The diagram below illustrates the lifecycle of a booking request and the interaction between layers:

1. **Presentation Layer**  
   - CLI Menu (`presentation/menu.py`) where users interact with the system.  
   - Flask REST API (`presentation/app.py`) exposing HTTP endpoints.
   - Handles input, displays output, and forwards requests to the Application Layer.

2. **Application Layer**  
   - Services (`BookingService`, `SpaceService`, `UserService`) orchestrate business logic.  
   - Validates user actions, manages booking operations, and interacts with the Domain Layer.

3. **Domain Layer**  
   - Core models and rules (`Booking`, `Space`, `User`).  
   - Encapsulates business logic, validations, and domain-specific constraints.

4. **Infrastructure Layer**  
   - Repositories (`BookingRepository`, `SpaceRepository`, `UserRepository`).  
   - Handles data persistence using a **SQLite relational database** (`smartspaces.db`).

The flow of a request is as follows: the user interacts with the **Presentation Layer**, which communicates with the **Application Layer**, triggering **Domain Layer** logic, and finally storing or retrieving data via the **Infrastructure Layer**. The response follows the reverse path back to the user.

![Smart Spaces Lifecycle](./docs/img/smart_spaces_lifecycle.png)

> This layered design ensures that changes in one layer (e.g., switching from in-memory repositories to a database) have minimal impact on other layers.


📂 **Project Structure**
```text
SmartSpaces
 ┣ 📜CHANGELOG.md               # Record of project changes and versions
 ┣ 📜README.md                  # Main project documentation
 ┣ 📜__init__.py                # Root package initializer
 ┣ 📜create_db.py                # Script to initialize and seed the SQLite database
 ┣ 📜smartspaces.db             # SQLite database file (auto-generated by create_db.py)
 ┣ 📂application                # Application layer: orchestrates business logic and use cases
 ┃ ┣ 📜booking_service.py       # Services related to bookings
 ┃ ┣ 📜space_service.py         # Services related to space management
 ┃ ┣ 📜user_service.py          # Services related to user management
 ┃ ┣ 📜__init__.py              # Package initializer for the application layer
 ┣ 📂docs                       # Project documentation
 ┃ ┣ 📜BUSINESS_RULES.md        # Document describing business rules
 ┃ ┣ 📜DESCRIPTION_AND_SCOPE.md # Document detailing project description and scope
 ┃ ┣ 📜DOMAIN_MODEL.md          # Domain model diagrams and explanations
 ┃ ┣ 📜EXECUTION.md             # Instructions for running the project
 ┃ ┣ 📜INITIAL_DATA.md          # Initial seed data for testing/demo
 ┃ ┣ 📜LAYERED_ARCHITECTURE.md  # Details about the layered architecture
 ┃ ┣ 📜README.md                # Documentation specific to docs folder
 ┃ ┣ 📜REPOSITORY_CONTRACT.md   # Repository interfaces/contracts
 ┃ ┣ 📜TESTS_AND_STEPS.md       # Steps for testing and test instructions
 ┃ ┣ 📜USE_CASES.md             # Description of main use cases
 ┃ ┗ 📂img                      # Images used in README and documentation
 ┣ 📂domain                     # Domain layer: core models and business rules
 ┃ ┣ 📜booking.py               # Booking model and logic
 ┃ ┣ 📜booking_repository.py    # Booking repository interface
 ┃ ┣ 📜space.py                 # Generic space model
 ┃ ┣ 📜space_meetingroom.py     # Specialized meeting room model
 ┃ ┣ 📜space_repository.py      # Space repository interface
 ┃ ┣ 📜user.py                  # User model
 ┃ ┣ 📜user_repository.py       # User repository interface
 ┃ ┣ 📜__init__.py              # Package initializer for the domain layer
 ┣ 📂infrastructure             # Infrastructure layer: concrete implementations of repositories
 ┃ ┣ 📜booking_memory_repository.py  # In-memory implementation of Booking repository
 ┃ ┣ 📜seed_data.py             # Script to populate initial data (in-memory)
 ┃ ┣ 📜space_memory_repository.py    # In-memory implementation of Space repository
 ┃ ┣ 📜user_memory_repository.py     # In-memory implementation of User repository
 ┃ ┣ 📜__init__.py              # Package initializer for infrastructure layer
 ┗ 📂presentation               # Presentation layer: user interface
   ┣ 📜menu.py                  # Console menu for user interaction
   ┣ 📜app.py                   # Flask REST API web interface
   ┗ 📜__init__.py              # Package initializer for presentation layer
```

---

🌳 **Workflow (Git Flow)**  
This project follows a branch-based development methodology, where each change is integrated via Pull Requests to
maintain traceability and code quality.

🔄 **Contribution Process**

1. Create a specific branch from `master` using the prefixes detailed below.
2. Make changes and commits following the naming standards.
3. Open a Pull Request (PR) describing the changes introduced.
4. Merge into the main branch after ensuring all tests pass successfully.

**Prefixes**

| Prefix    | Description                              |
|-----------|------------------------------------------|
| feature/  | New features and capabilities            |
| fix/      | Bug fixes and error corrections          |
| docs/     | Documentation updates and improvements   |
| refactor/ | Code improvements without changing logic |
| test/     | Adding or updating test cases            |

---

👤 **Author & Creator**  
Víctor Felipe Suárez – Architect and Developer of Smart Spaces

📄 **Version & Credits**  
Initial version developed as part of the Smart Spaces project. All code, documentation, and examples created by the
author.
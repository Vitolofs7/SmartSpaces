# Smart Spaces

## **Overview**

The project is an **Intelligent Space Management System** designed to manage and optimize the use of shared physical
spaces within an organization, such as classrooms, meeting rooms, workstations, or multipurpose rooms.

The system models reservable spaces and users with different roles, allowing **temporary bookings** while enforcing
rules based on both user type and space characteristics.

> Note: This project focuses on simulating the logical operation of the system, emphasizing **object-oriented design**,
> consistent operations, and correct relationships among model elements.

---

## **Objectives**

### **General Objective**

Develop a modular, object-oriented system that enables coherent management of shared spaces and bookings, avoiding
conflicts and ensuring compliance with usage rules.

### **Specific Objectives**

- Model users with different roles and capabilities.
- Represent physical spaces with specific characteristics and restrictions.
- Manage bookings while preventing overlaps and ensuring availability.
- Automatically enforce rules depending on user type and space type.
- Use inheritance and multiple inheritance to promote code reuse and system scalability.

---

## **Main Features**

### **User Management**

- Generic users with common attributes like ID and name.
- Different user types with specific rules:
    - Basic users: strict booking limits.
    - Premium users: more flexible booking rules.
    - Administrators: global system management capabilities.
- Each user type can define:
    - Maximum number of active bookings.
    - Maximum allowed booking duration.
- Additional behaviors can be added via multiple inheritance (e.g., booking priority) without duplicating code.

### **Space Management**

- Spaces represent **physical resources** available for reservation.
- Different types of spaces:
    - Classrooms
    - Meeting rooms
    - Workstations
    - Multipurpose rooms
- Common attributes: ID, name, capacity, status (available, reserved, maintenance).
- Specific space types can define additional rules through inheritance.

### **Advanced Features for Spaces**

- Spaces can include **special features**, implemented via multiple inheritance:
    - Equipment (projector, video conference, sound systems)
    - Time restrictions
    - Premium access rules
- A single space can belong to a functional category and have extra features, avoiding rigid class hierarchies.

### **Bookings and Availability Control**

- Bookings link a user to a space for a specific time interval.
- Automatic checks:
    - Space availability
    - No overlaps with existing bookings
    - User permissions
    - Compliance with space-specific rules
- Booking statuses: active, canceled, finished.

---

## **Object-Oriented Design**

The project follows core OOP principles:

- **Encapsulation**: Protect data and validate operations.
- **Inheritance**: Model different types of users and spaces.
- **Multiple inheritance**: Add extra behaviors like priority, equipment, or time restrictions.
- **Polymorphism**: Handle different types uniformly.

---

## **Available Actions**

The system supports:

- Registering, modifying, and deleting users.
- Registering, modifying, and deactivating spaces.
- Checking space availability.
- Creating, canceling, and finishing bookings.
- Listing active bookings by user or by space.
- Preventing invalid operations (overlapping bookings, unauthorized access).

---

## **Installation & Execution**

### **Requirements**

- Python 3.9+
- No external dependencies are required (all in-memory for simulation).

### **Installation**

1. Clone the repository:

```bash
git clone <repository_url>
cd SmartSpaces
```

2. The project uses only standard Python libraries, so no additional packages are required.

### **Running the Application**

From the project root, execute the menu module:

```bash
python -m presentation.menu
```

- Use the interactive menu to list spaces, users, bookings, or perform actions like creating, canceling, or finishing
  bookings.

- The system will automatically enforce booking rules and space availability constraints.

### **Project Scope**

## **Includes**

- Modeling of users, spaces, and bookings.

- Management of different types of users and spaces with specific behaviors.

- Use of inheritance and multiple inheritance for scalable design.

- State control and validation to enforce usage rules.

- Checks to prevent inconsistent or invalid operations (e.g., overlapping bookings).

## **Excludes**

- Graphical or web interfaces.

- Database or file persistence (all data is in-memory).

- Integration with external services (payments, notifications, sensors).

Contributing

Fork the repository and create a feature branch (git checkout -b feature/my-feature).

Commit your changes (git commit -am 'Add new feature').

Push to the branch (git push origin feature/my-feature).

Open a Pull Request and describe your changes.
## **Overview**
The project consists of the design and development of an **Intelligent Space Management System**, aimed at the administration and optimization of the use of shared physical spaces within an organization, such as classrooms, meeting rooms, workstations, or multipurpose rooms.

The system models a set of reservable spaces and a set of users with different roles, allowing the management of **temporary bookings** for these spaces under a series of rules and restrictions defined by the system itself. These rules are applied automatically based on both the type of user and the characteristics of the reserved space.

Although the project is inspired by real applications used in companies, universities, or coworking spaces, its main objective is to **simulate the logical operation of the system**, focusing on object-oriented design, operation consistency, and the correct relationships among the model elements.

## **Objectives**
### **General Objective**
Develop a modular, object-oriented system that allows coherent management of shared spaces and their bookings, avoiding conflicts and ensuring compliance with the established usage rules.

### **Specific Objectives**
- Model users with different roles and capabilities within the system.
- Represent physical spaces with differentiated characteristics and restrictions.
- Manage bookings, ensuring space availability and avoiding overlaps.
- Apply automatic rules depending on the user type and the type of space.
- Use inheritance and multiple inheritance to promote code reuse and system scalability.

## **Main Features**
### **User Management**
- The system will include **generic users** with common information, such as ID and name.
- **Different types of users** will be defined, for example:
  - Basic users, with strict usage limits.
  - Premium users, with greater booking flexibility.
  - Administrators, with global system management permissions.
- Each user type will have its own rules, such as:
  - Maximum number of active bookings.
  - Maximum allowed booking duration.
- Through multiple inheritance, a user can incorporate **additional behaviors**, such as booking priority or extended limits, without duplicating code.

### **Space Management**
- Spaces will represent the **physical resources available for reservation** within the organization.
- **Different types of spaces** will be managed, such as:
  - Classrooms.
  - Meeting rooms.
  - Workstations.
  - Multipurpose rooms.
- Each space will include common information like ID, name, capacity, and status (available, reserved, or under maintenance).
- Through inheritance, each space type can define specific usage rules.

### **Advanced Features and Multiple Inheritance in Spaces**
In addition to the basic space type, some spaces may include **additional features**, implemented using multiple inheritance:

- Spaces with special equipment (projector, video conferencing systems, sound).
- Spaces with time restrictions.
- Premium spaces with specific access conditions.

In this way, a single space can belong to a functional category while also having additional features, avoiding rigid and non-scalable class hierarchies.

### **Bookings and Availability Control**
- **Bookings** link a user to a space for a specific time interval.
- The system will automatically check:
  - Space availability.
  - Absence of overlaps with other bookings.
  - That the user has the necessary permissions.
  - Compliance with space-specific rules.
- Bookings can have different statuses, such as active, canceled, or finished.

## **Object-Oriented Design**
The project will follow core Object-Oriented Programming principles:

- **Encapsulation**, to protect data and control valid operations.
- **Inheritance**, to model different types of users and spaces from base classes.
- **Multiple inheritance**, to add additional behaviors such as priority, equipment, or time restrictions.
- **Polymorphism**, allowing uniform handling of different types of users and spaces.

## **Available Actions and Queries**
The system will allow, among other things:

- Registering, modifying, and deleting users.
- Registering, modifying, and deactivating spaces.
- Checking space availability.
- Creating, canceling, and finishing bookings.
- Listing active bookings by user or by space.
- Detecting and preventing invalid operations, such as overlapping bookings or unauthorized access.

## **Project Scope**
### **Includes**
- Modeling of users, spaces, and bookings.
- Management of different types of users and spaces with differentiated behaviors.
- Implementation of inheritance and multiple inheritance where justified.
- State control and validation of usage rules.
- Checks to prevent inconsistent states or operations.

### **Excludes**
- Graphical interfaces or web applications.
- Database persistence.
- Integration with external payment systems, sensors, or notifications.

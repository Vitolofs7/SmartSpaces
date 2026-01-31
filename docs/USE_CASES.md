# Use Cases

This document describes the functional **use cases** of the Smart Spaces system based on the options available in the
command-line menu. Each use case is described from the user's point of view, including inputs, validations, outputs, and
possible errors.

---

## UC-1: List Spaces

### Description

Displays all spaces registered in the system. Each space is shown with its basic information, and if the space is a
meeting room, its specific attributes are also displayed.

### Input

- None (menu option `1`)

### Validations

- None

### Output

- A list of spaces printed to the console.
- For all spaces:
    - ID
    - Name
    - Type
    - Status
    - Capacity
- For meeting rooms, additional information:
    - Room number
    - Floor
    - Number of power outlets
    - Equipment list

### Errors

- None

---

## UC-2: List Users

### Description

Displays all users currently registered in the system and their active status.

### Input

- None (menu option `2`)

### Validations

- None

### Output

- A list of users showing:
    - User ID
    - Full name
    - Whether the user is active

### Errors

- None

---

## UC-3: List Bookings

### Description

Displays all bookings stored in the system.

### Input

- None (menu option `3`)

### Validations

- None

### Output

- A list of bookings showing:
    - Booking ID
    - User name
    - Space name
    - Booking status

### Errors

- None

---

## UC-4: Create Booking

### Description

Creates a new booking for a specific space and user during a defined time interval.

### Input

- User ID
- Space ID
- Start datetime
- End datetime

### Validations

- User exists
- Space exists
- Datetime format is valid
- Start datetime is before end datetime
- Space is available during the selected period
- No overlapping bookings exist
- Domain booking rules are satisfied

### Output

- Confirmation message indicating the booking was successfully created
- Generated booking ID

### Errors

- `ValueError` if:
    - User ID does not exist
    - Space ID does not exist
    - Date format is invalid
    - End time is before start time
    - The space is not available
    - Business rules are violated

---

## UC-5: Cancel Booking

### Description

Cancels an existing booking.

### Input

- Booking ID

### Validations

- Booking exists
- Booking can be canceled based on its current status

### Output

- Confirmation message indicating the booking has been canceled

### Errors

- `ValueError` if:
    - Booking ID does not exist
    - Booking cannot be canceled

---

## UC-6: Finish Booking

### Description

Marks an active booking as finished and releases the associated space.

### Input

- Booking ID

### Validations

- Booking exists
- Booking is currently active

### Output

- Confirmation message indicating the booking has been finished

### Errors

- `ValueError` if:
    - Booking ID does not exist
    - Booking is not in an active state

---

## UC-7: Create Space

### Description

Creates a new space in the system. The user can choose between creating a generic space or a meeting room.

### Input

- Space type selection:
    - Generic space
    - Meeting room
- Space ID
- Space name
- Capacity
- If meeting room:
    - Room number
    - Floor
    - Number of power outlets
    - Optional equipment list

### Validations

- Space ID is not empty
- Space name is not empty
- Capacity is greater than zero
- For meeting rooms:
    - Floor is valid
    - Number of power outlets is non-negative
- Space ID does not already exist

### Output

- Confirmation message indicating the space was created successfully

### Errors

- `ValueError` if:
    - Any required value is invalid
    - Capacity is not a positive number
    - Space ID already exists
- User input error if an invalid space type is selected

---

## UC-8: Exit Application

### Description

Terminates the execution of the Smart Spaces application.

### Input

- None (menu option `8`)

### Validations

- None

### Output

- Exit message
- Application closes

### Errors

- None

---

## Error Handling

All validation and business rule violations are handled using `ValueError`.  
These exceptions are caught in the presentation layer and displayed to the user as readable error messages, ensuring
controlled execution and preventing application crashes.

---

## Notes

- The presentation layer handles user input and output.
- Business logic and validations are delegated to the application and domain layers.
- Repositories provide in-memory persistence for the system entities.

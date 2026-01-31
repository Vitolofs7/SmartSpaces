# Execution Guide

## Requirements

To execute the Smart Spaces project, the following requirements are needed:

- **Python 3.9 or higher**
- A terminal or command-line interface
- No external libraries or frameworks are required

The application uses only the Python standard library and runs entirely in memory.

---

## How to Execute the Menu

1. Open a terminal.
2. Navigate to the root directory of the project (where the `presentation` folder is located).
3. Run the following command:

```bash
python -m presentation.menu
```

After executing this command, the main menu of the Smart Spaces system will be displayed.

---

## Main Menu Options

Once the application is running, the user can interact with the system through the following options:

1. List spaces

2. List users

3. List bookings

4. Create booking

5. Cancel booking

6. Finish booking

7. Create Space

8. Exit

Each option is selected by typing its number and pressing Enter.

# Example Execution Flows

## Example 1: Listing Spaces

1. Start the application.
2. Select option `1` (List spaces).
3. The system displays all registered spaces, including:
    * Space ID
    * Name
    * Type of space
    * Status
    * Capacity
4. If a space belongs to a specialized type (e.g. meeting room), its specific attributes such as room number, floor,
   power outlets, and equipment are also shown.

This allows the user to clearly understand the available spaces and their characteristics.

## Example 2: Creating a Booking

1. Select option `4` (Create booking).
2. Enter a valid User ID.
3. Enter a valid Space ID.
4. Enter the start and end date and time using one of the accepted formats:
    * `YYYY-MM-DD HH:MM`
    * `YYYY/MM/DD HH:MM`
5. The system checks:
    * Space availability
    * Booking overlaps
    * Validity of the user and space
6. If all rules are satisfied, the booking is created successfully and confirmed on screen.

## Example 3: Canceling a Booking

1. Select option `5` (Cancel booking).
2. Enter the booking ID.
3. If the booking exists and is active, it is canceled.
4. The system confirms the cancellation.

## Example 4: Finishing a Booking

1. Select option `6` (Finish booking).
2. Enter the booking ID.
3. The booking status is updated to finished.
4. The system confirms the operation.

## Error Handling During Execution

If the user performs an invalid action (such as entering an incorrect date format, selecting a non-existent ID, or
attempting an invalid booking), the system will:

* Reject the operation
* Display an explanatory error message
* Return safely to the main menu

## Execution Notes

* All data is stored in memory and is reset each time the program is executed.
* The system is designed for single-user, sequential interaction.
* To exit the application safely, select option `8` (Exit).

## Summary

The Smart Spaces menu provides a simple, guided way to interact with the system, allowing users to explore spaces,
manage bookings, and validate the system's behavior through a clear command-line interface.

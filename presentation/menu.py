"""presentation/menu.py"""

from datetime import datetime
from infrastructure.space_sqlite_repository import SpaceSQLiteRepository
from infrastructure.user_sqlite_repository import UserSQLiteRepository
from infrastructure.booking_sqlite_repository import BookingSQLiteRepository
from application.booking_service import BookingService
from application.space_service import SpaceService
from application.user_service import UserService
from infrastructure.seed_data_sqlite import seed_all


def show_menu():
    """Displays the main menu options."""
    print("\n=== SMART SPACES MENU ===")
    print("\n".join([
        "1. List spaces",
        "2. List users",
        "3. List bookings",
        "4. Create booking",
        "5. Cancel booking",
        "6. Finish booking",
        "7. Create space",
        "8. List available spaces",
        "9. Modify booking",
        "10. Exit"
    ]))


def parse_datetime(value: str) -> datetime:
    for fmt in ("%Y-%m-%d %H:%M", "%Y/%m/%d %H:%M"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError("Invalid date format. Use YYYY-MM-DD HH:MM or YYYY/MM/DD HH:MM")


def select_user(user_service):
    print("\nAvailable users:")
    for user in user_service.list_users():
        print(user.full_name())
    return input("Choose user name: ").strip()


def select_space(space_service):
    print("\nAvailable spaces:")
    for space in space_service.list_spaces():
        print(space.space_name)
    return input("Choose space name: ").strip()


def input_dates():
    print("\nEnter booking dates. (YYYY-MM-DD HH:MM or YYYY/MM/DD HH:MM)")
    start = parse_datetime(input("Start datetime: ").strip())
    end = parse_datetime(input("End datetime: ").strip())
    return start, end


def create_space(space_service):
    print("\nSelect space type:\n1. Generic space\n2. Meeting room")
    space_type = input("Choose type: ").strip()
    space_name = input("Space name: ").strip()
    capacity = int(input("Capacity: ").strip())

    if space_type == "1":
        space_service.create_space(space_name, capacity, "Basic")
    elif space_type == "2":
        room_number = input("Room number: ").strip()
        floor = int(input("Floor: ").strip())
        num_power_outlets = int(input("Number of power outlets: ").strip())
        equipment_raw = input("Equipment list (comma separated, optional): ").strip()
        equipment_list = [e.strip() for e in equipment_raw.split(",")] if equipment_raw else []
        space_service.create_meeting_room(space_name, capacity, room_number, floor, num_power_outlets, equipment_list)
    else:
        print("Invalid space type.")
        return
    print("\nSpace created successfully.")


def main():
    """Main entry point for the Smart Spaces menu-driven application."""
    DB_PATH = "smartspaces.db"

    space_repo   = SpaceSQLiteRepository(DB_PATH)
    user_repo    = UserSQLiteRepository(DB_PATH)
    booking_repo = BookingSQLiteRepository(DB_PATH)

    booking_service = BookingService(booking_repo, space_repo, user_repo)
    space_service   = SpaceService(space_repo, booking_repo)
    user_service    = UserService(user_repo)

    seed_all(space_repo, user_repo, booking_repo)

    while True:
        show_menu()
        option = input("Choose an option: ").strip()
        try:
            if option == "1":
                for space in space_service.list_spaces():
                    print(space)
            elif option == "2":
                for user in user_service.list_users():
                    print(f"{user.user_id} - {user.full_name()} - Active: {user.is_active()}")
            elif option == "3":
                for booking in booking_service.list_bookings():
                    print(f"{booking.booking_id} - {booking.user.full_name()} booked {booking.space.space_name} from {booking.start_time} to {booking.end_time} - Status: {booking.status}")
            elif option == "4":
                user_name  = select_user(user_service)
                space_name = select_space(space_service)
                start, end = input_dates()
                booking = booking_service.create_booking(user_name, space_name, start, end)
                print(f"\nBooking {booking.booking_id} created successfully")
            elif option == "5":
                booking_service.cancel_booking(input("Booking ID to cancel: ").strip())
                print("Booking cancelled.")
            elif option == "6":
                booking_service.finish_booking(input("Booking ID to finish: ").strip())
                print("Booking finished.")
            elif option == "7":
                create_space(space_service)
            elif option == "8":
                start, end = input_dates()
                available_spaces = space_service.get_available_spaces(start, end)
                if not available_spaces:
                    print("No spaces available for the selected dates.")
                else:
                    print("\nAvailable spaces:")
                    for space in available_spaces:
                        print(space)
            elif option == "9":
                booking_id = input("Enter booking ID to modify: ").strip()
                new_start, new_end = input_dates()
                booking = booking_service.modify_booking(booking_id, new_start, new_end)
                print(f"Booking {booking.booking_id} rescheduled to {booking.start_time} - {booking.end_time}")
            elif option == "10":
                print("Goodbye!")
                break
            else:
                print("Invalid option.")
        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
# presentation/menu.py
from datetime import datetime
from infrastructure.space_memory_repository import SpaceMemoryRepository
from infrastructure.user_memory_repository import UserMemoryRepository
from infrastructure.booking_memory_repository import BookingMemoryRepository
from application.booking_service import BookingService
from application.space_service import SpaceService
from application.user_service import UserService
from infrastructure.seed_data import seed_all


def show_menu():
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
    for u in user_service.list_users():
        print(u.full_name())
    return input("Choose user name: ").strip()


def select_space(space_service):
    print("\nAvailable spaces:")
    for s in space_service.list_spaces():
        print(s.space_name)
    return input("Choose space name: ").strip()


def input_dates():
    print("\nEnter booking dates. (YYYY-MM-DD HH:MM or YYYY/MM/DD HH:MM)")
    start = parse_datetime(input("Start datetime: ").strip())
    end = parse_datetime(input("End datetime: ").strip())
    return start, end


def create_space(space_service):
    print("\nSelect space type:\n1. Generic space\n2. Meeting room")
    space_type = input("Choose type: ").strip()
    space_id, space_name, capacity = input("Space ID: ").strip(), input("Space name: ").strip(), int(
        input("Capacity: ").strip())
    if space_type == "1":
        space_service.create_space(space_id, space_name, capacity, "Basic")
    elif space_type == "2":
        room_number, floor, num_power_outlets = input("Room number: ").strip(), int(input("Floor: ").strip()), int(
            input("Number of power outlets: ").strip())
        equipment_raw = input("Equipment list (comma separated, optional): ").strip()
        equipment_list = [e.strip() for e in equipment_raw.split(",")] if equipment_raw else []
        space_service.create_meeting_room(space_id, space_name, capacity, room_number, floor, num_power_outlets,
                                          equipment_list)
    else:
        print("Invalid space type.")
        return
    print("\nSpace created successfully.")


def main():
    # Initialize repositories and services
    space_repo = SpaceMemoryRepository()
    user_repo = UserMemoryRepository()
    booking_repo = BookingMemoryRepository()
    booking_service = BookingService(booking_repo, space_repo, user_repo)
    space_service = SpaceService(space_repo)
    user_service = UserService(user_repo)
    seed_all(space_repo, user_repo, booking_repo)

    while True:
        show_menu()
        option = input("Choose an option: ").strip()
        try:
            if option == "1":
                print("\n".join(str(s) for s in space_service.list_spaces()))
            elif option == "2":
                print("\n".join(
                    f"{u.user_id} - {u.full_name()} - Active: {u.is_active()}" for u in user_service.list_users()))
            elif option == "3":
                print("\n".join(
                    f"{b.booking_id} - {b.user.full_name()} - {b.space.space_name} - Status: {b.status}" for b in
                    booking_service.list_bookings()))
            elif option == "4":
                user_name = select_user(user_service)
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
                available_spaces = space_service.get_available_spaces(booking_repo, start, end)
                if not available_spaces:
                    print("No spaces available for the selected dates.")
                else:
                    print("\nAvailable spaces:")
                    for s in available_spaces:
                        print(s)
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

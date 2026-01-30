# presentation/menu.py
from datetime import datetime, timedelta

# Repositorios
from infrastructure.space_memory_repository import SpaceMemoryRepository
from infrastructure.user_memory_repository import UserMemoryRepository
from infrastructure.booking_memory_repository import BookingMemoryRepository

# Servicio
from application.booking_service import BookingService

# Dominio
from domain.space import Space
from domain.user import User
from domain.space_meetingroom import SpaceMeetingroom

# Data
from infrastructure.seed_data import seed_all


def mostrar_menu():
    print("\n=== SMART SPACES MENU ===")
    print("1. List spaces")
    print("2. List users")
    print("3. List bookings")
    print("4. Create booking")
    print("5. Cancel booking")
    print("6. Finish booking")
    print("7. Create space")
    print("8. Exit")


def parse_datetime(value: str) -> datetime:
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y/%m/%d %H:%M",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass
    raise ValueError(
        "Invalid date format. Please use YYYY-MM-DD HH:MM or YYYY/MM/DD HH:MM"
    )


def main():
    # Crear repositorios y servicio
    space_repo = SpaceMemoryRepository()
    user_repo = UserMemoryRepository()
    booking_repo = BookingMemoryRepository()
    service = BookingService(booking_repo, space_repo, user_repo)

    # Datos de ejemplo
    seed_all(space_repo, user_repo)

    while True:
        mostrar_menu()
        opcion = input("Choose an option: ").strip()

        try:
            if opcion == "1":
                print("\nSpaces:")
                for s in space_repo.list():
                    print(s)

            elif opcion == "2":
                print("\nUsers:")
                for u in user_repo.list():
                    print(f"{u.user_id} - {u.full_name()} - Active: {u.is_active()}")

            elif opcion == "3":
                print("\nBookings:")
                for b in service.list_bookings():
                    print(f"{b.booking_id} - {b._user.name} - {b._space.space_name} - Status: {b._booking_status}")

            elif opcion == "4":
                user_id = input("User ID: ").strip()
                space_id = input("Space ID: ").strip()

                print("\nEnter booking dates.")
                print("Accepted formats:")
                print(" - YYYY-MM-DD HH:MM")
                print(" - YYYY/MM/DD HH:MM")

                start = parse_datetime(
                    input("Start datetime: ").strip()
                )
                end = parse_datetime(
                    input("End datetime: ").strip()
                )

                booking_id = f"B{len(service.list_bookings()) + 1}"

                booking = service.create_booking(
                    booking_id=booking_id,
                    user_id=user_id,
                    space_id=space_id,
                    start_time=start,
                    end_time=end,
                )

                print(f"\nBooking {booking.booking_id} created successfully")

            elif opcion == "5":
                booking_id = input("Booking ID to cancel: ").strip()
                service.cancel_booking(booking_id)
                print("Booking cancelled.")

            elif opcion == "6":
                booking_id = input("Booking ID to finish: ").strip()
                service.finish_booking(booking_id)
                print("Booking finished.")

            elif opcion == "7":
                print("\nSelect space type:")
                print("1. Generic space")
                print("2. Meeting room")
                space_type = input("Choose type: ").strip()

                space_id = input("Space ID: ").strip()
                space_name = input("Space name: ").strip()
                capacity = int(input("Capacity: ").strip())

                if space_type == "1":
                    space = Space(space_id, space_name, capacity, space_type)

                elif space_type == "2":
                    room_number = input("Room number: ").strip()
                    floor = int(input("Floor: ").strip())
                    num_power_outlets = int(input("Number of power outlets: ").strip())
                    equipment_raw = input(
                        "Equipment list (comma separated, optional): "
                    ).strip()
                    equipment_list = (
                        [e.strip() for e in equipment_raw.split(",")]
                        if equipment_raw
                        else []
                    )

                    space = SpaceMeetingroom(
                        space_id=space_id,
                        space_name=space_name,
                        capacity=capacity,
                        room_number=room_number,
                        floor=floor,
                        num_power_outlets=num_power_outlets,
                        equipment_list=equipment_list,
                    )
                else:
                    print("Invalid space type.")
                    continue

                space_repo.save(space)
                print("\nSpace created successfully.")

            elif opcion == "8":
                print("Goodbye!")
                break

            else:
                print("Invalid option.")

        except ValueError as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

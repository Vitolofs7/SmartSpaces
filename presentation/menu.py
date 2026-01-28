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
    print("7. Exit")

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
                    print(f"{s.space_id} - {s.space_name} - Status: {s.space_status} - Capacity: {s.capacity}")

            elif opcion == "2":
                print("\nUsers:")
                for u in user_repo.list():
                    print(f"{u.user_id} - {u.name} - Active: {u.is_active()}")

            elif opcion == "3":
                print("\nBookings:")
                for b in service.list_bookings():
                    print(f"{b.booking_id} - {b._user.name} - {b._space.space_name} - Status: {b._booking_status}")

            elif opcion == "4":
                user_id = input("User ID: ").strip()
                space_id = input("Space ID: ").strip()
                start_str = input("Start datetime (YYYY-MM-DD HH:MM): ").strip()
                end_str = input("End datetime (YYYY-MM-DD HH:MM): ").strip()

                start_time = datetime.strptime(start_str, "%Y-%m-%d %H:%M")
                end_time = datetime.strptime(end_str, "%Y-%m-%d %H:%M")

                booking_id = f"B{len(service.list_bookings()) + 1}"
                booking = service.create_booking(booking_id, user_id, space_id, start_time, end_time)
                print(f"Booking created: {booking.booking_id} - Status: {booking._booking_status}")

            elif opcion == "5":
                booking_id = input("Booking ID to cancel: ").strip()
                service.cancel_booking(booking_id)
                print("Booking cancelled.")

            elif opcion == "6":
                booking_id = input("Booking ID to finish: ").strip()
                service.finish_booking(booking_id)
                print("Booking finished.")

            elif opcion == "7":
                print("Goodbye!")
                break

            else:
                print("Invalid option.")

        except ValueError as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

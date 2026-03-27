"""infrastructure/seed_data_sqlite.py"""

from datetime import datetime, timedelta
from domain.space import Space
from domain.space_meetingroom import SpaceMeetingRoom
from domain.user import User
from domain.booking import Booking
from infrastructure.user_sqlite_repository import UserSQLiteRepository
from infrastructure.space_sqlite_repository import SpaceSQLiteRepository
from infrastructure.booking_sqlite_repository import BookingSQLiteRepository


def seed_spaces(space_repo: SpaceSQLiteRepository):
    spaces = [
        Space("S1", "Conference Room", 5, "Basic"),
        Space("S2", "Open Space", 10, "Basic"),
        SpaceMeetingRoom("S3", "Main Meeting Room", 8, "101", 1, ["Projector", "Whiteboard"], 4),
        SpaceMeetingRoom("S4", "Small Meeting Room", 4, "102", 1, ["TV"], 2),
        Space("S5", "Private Office", 2, "Private"),
    ]
    for s in spaces:
        try:
            space_repo.save(s)
        except Exception as e:
            print(f"Error guardando espacio {s.space_id}: {e}")


def seed_users(user_repo: UserSQLiteRepository):
    users = [
        User("U1", "Alice", "Smith", "Johnson"),
        User("U2", "Bob", "Brown", "Taylor"),
        User("U3", "Charlie", "Wilson", "Anderson"),
        User("U4", "Diana", "Martinez", "Lopez"),
        User("U5", "Eve", "Davis", "Clark"),
    ]
    for u in users:
        try:
            user_repo.save(u)
        except Exception as e:
            print(f"Error guardando usuario {u.user_id}: {e}")


def seed_bookings(booking_repo: BookingSQLiteRepository, space_repo: SpaceSQLiteRepository, user_repo: UserSQLiteRepository):
    now = datetime.now()
    bookings_data = [
        ("U1", "S1", now + timedelta(hours=1), now + timedelta(hours=2)),
        ("U2", "S3", now + timedelta(days=1), now + timedelta(days=1, hours=2)),
        ("U3", "S2", now + timedelta(hours=3), now + timedelta(hours=5)),
    ]
    for user_id, space_id, start, end in bookings_data:
        try:
            user = user_repo.get(user_id)
            space = space_repo.get(space_id)
            Booking.create(space, user, start, end, booking_repo)
        except Exception as e:
            print(f"Error creando reserva para usuario {user_id} en espacio {space_id}: {e}")


def seed_all(space_repo, user_repo, booking_repo):
    # Si ya hay espacios, la BD fue inicializada por create_db.py — no hacer nada
    if space_repo.list():
        return
    seed_spaces(space_repo)
    seed_users(user_repo)
    seed_bookings(booking_repo, space_repo, user_repo)
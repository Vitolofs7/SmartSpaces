# infrastructure/seed_data.py

from datetime import datetime, timedelta
from domain.space import Space
from domain.space_meetingroom import SpaceMeetingroom
from domain.user import User
from domain.booking import Booking
from infrastructure.space_memory_repository import SpaceMemoryRepository
from infrastructure.user_memory_repository import UserMemoryRepository
from infrastructure.booking_memory_repository import BookingMemoryRepository

def seed_spaces(space_repo: SpaceMemoryRepository):
    """Seeds the space repository with sample spaces.

    Includes generic spaces and meeting rooms with different capacities and equipment.

    Args:
        space_repo: The in-memory space repository to populate.
    """
    spaces = [
        Space("S1", "Conference Room", 5, "Basic"),
        Space("S2", "Open Space", 10, "Basic"),
        SpaceMeetingroom("S3", "Main Meeting Room", 8, "101", 1, ["Projector", "Whiteboard"], 4),
        SpaceMeetingroom("S4", "Small Meeting Room", 4, "102", 1, ["TV"], 2),
        Space("S5", "Private Office", 2, "Private"),
    ]
    for s in spaces:
        space_repo.save(s)

def seed_users(user_repo: UserMemoryRepository):
    """Seeds the user repository with sample users.

    Args:
        user_repo: The in-memory user repository to populate.
    """
    users = [
        User("U1", "Alice", "Smith", "Johnson"),
        User("U2", "Bob", "Brown", "Taylor"),
        User("U3", "Charlie", "Wilson", "Anderson"),
        User("U4", "Diana", "Martinez", "Lopez"),
        User("U5", "Eve", "Davis", "Clark"),
    ]
    for u in users:
        user_repo.save(u)

def seed_bookings(booking_repo: BookingMemoryRepository, space_repo, user_repo):
    """Seeds the booking repository with sample bookings.

    Creates bookings for existing users and spaces with specific start and end times.

    Args:
        booking_repo: The in-memory booking repository to populate.
        space_repo: Repository to fetch spaces.
        user_repo: Repository to fetch users.
    """
    now = datetime.now()
    bookings_data = [
        ("U1", "S1", now + timedelta(hours=1), now + timedelta(hours=2)),
        ("U2", "S3", now + timedelta(days=1), now + timedelta(days=1, hours=2)),
        ("U3", "S2", now + timedelta(hours=3), now + timedelta(hours=5)),
    ]
    for user_id, space_id, start, end in bookings_data:
        user = user_repo.get(user_id)
        space = space_repo.get(space_id)
        if user and space:
            Booking.create(space, user, start, end, booking_repo)

def seed_all(space_repo: SpaceMemoryRepository, user_repo: UserMemoryRepository, booking_repo: BookingMemoryRepository):
    """Seeds all repositories with initial sample data.

    Populates spaces, users, and bookings in the given repositories.

    Args:
        space_repo: Space repository to seed.
        user_repo: User repository to seed.
        booking_repo: Booking repository to seed.
    """
    seed_spaces(space_repo)
    seed_users(user_repo)
    seed_bookings(booking_repo, space_repo, user_repo)

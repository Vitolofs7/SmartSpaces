# infrastructure/seed_data.py

from domain.space import Space
from domain.user import User
from infrastructure.space_memory_repository import SpaceMemoryRepository
from infrastructure.user_memory_repository import UserMemoryRepository

def seed_spaces(space_repo: SpaceMemoryRepository):
    """Adds initial spaces to the repository."""
    spaces = [
        Space("S1", "Conference Room", 5),
        Space("S2", "Meeting Room", 3),
        Space("S3", "Open Space", 10),
        Space("S4", "Private Office", 2),
    ]
    for s in spaces:
        space_repo.save(s)

def seed_users(user_repo: UserMemoryRepository):
    """Adds initial users to the repository."""
    users = [
        User("U1", "Alice"),
        User("U2", "Bob"),
        User("U3", "Charlie"),
        User("U4", "Diana"),
    ]
    for u in users:
        user_repo.save(u)

def seed_all(space_repo: SpaceMemoryRepository, user_repo: UserMemoryRepository):
    """Seeds both spaces and users."""
    seed_spaces(space_repo)
    seed_users(user_repo)

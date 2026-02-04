# infrastructure/seed_data.py

from domain.space import Space
from domain.space_meetingroom import SpaceMeetingroom
from domain.user import User
from infrastructure.space_memory_repository import SpaceMemoryRepository
from infrastructure.user_memory_repository import UserMemoryRepository


def seed_spaces(space_repo: SpaceMemoryRepository):
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
    users = [
        User("U1", "Alice", "Smith", "Johnson"),
        User("U2", "Bob", "Brown", "Taylor"),
        User("U3", "Charlie", "Wilson", "Anderson"),
        User("U4", "Diana", "Martinez", "Lopez"),
        User("U5", "Eve", "Davis", "Clark"),
    ]
    for u in users:
        user_repo.save(u)


def seed_all(space_repo: SpaceMemoryRepository, user_repo: UserMemoryRepository):
    seed_spaces(space_repo)
    seed_users(user_repo)

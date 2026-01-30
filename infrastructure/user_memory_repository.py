# infrastructure/user_memory_repository.py

from domain.user_repository import UserRepository


class UserMemoryRepository(UserRepository):
    """In-memory implementation of the UserRepository interface."""

    def __init__(self):
        """Initializes an empty in-memory data store for users."""
        self._data = {}

    def save(self, user):
        """Saves a user in memory.

        Args:
            user: The User instance to save.
        """
        self._data[user.user_id] = user

    def get(self, user_id):
        """Retrieves a user by their ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            The User instance if found, or None otherwise.
        """
        return self._data.get(user_id)

    def list(self):
        """Returns all users stored in memory.

        Returns:
            A list of all User instances.
        """
        return list(self._data.values())

    def delete(self, user_id):
        """Deletes a user from memory by their ID.

        Args:
            user_id: The ID of the user to delete.
        """
        self._data.pop(user_id, None)

# infrastructure/user_memory_repository.py

from domain.user_repository import UserRepository


class UserMemoryRepository(UserRepository):
    """In-memory implementation of the UserRepository interface.

    Stores users in a dictionary using their IDs as keys. Useful for testing
    or scenarios without a persistent storage backend.
    """

    def __init__(self):
        """Initializes an empty in-memory user repository."""
        self._data = {}

    def save(self, user):
        """Stores or updates a user in memory.

        Args:
            user: User instance to save.
        """
        self._data[user.user_id] = user

    def get(self, user_id):
        """Retrieves a user by its ID.

        Args:
            user_id: Unique identifier of the user.

        Returns:
            The user instance if found, otherwise None.
        """
        return self._data.get(user_id)

    def list(self):
        """Retrieves all stored users.

        Returns:
            A list of all user instances.
        """
        return list(self._data.values())

    def delete(self, user_id):
        """Deletes a user by its ID if it exists.

        Args:
            user_id: Unique identifier of the user to delete.
        """
        self._data.pop(user_id, None)

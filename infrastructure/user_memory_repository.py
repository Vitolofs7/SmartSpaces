"""infrastructure/user_memory_repository.py"""

from domain.user_repository import UserRepository
from domain.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundError,
)


class UserMemoryRepository(UserRepository):
    """In-memory implementation of the UserRepository interface.

    Stores users in a dictionary using their IDs as keys. Useful for testing
    or scenarios without a persistent storage backend.
    """

    def __init__(self):
        """Initializes an empty in-memory user repository."""
        self._users = {}

    def save(self, user):
        """Stores a new user in memory.

        Args:
            user: User instance to save.
            
        Raises:
            UserAlreadyExistsException: If the user already exists.
        """
        if user.user_id in self._users:
            raise UserAlreadyExistsException(f"Ya existe un usuario con ID '{user.user_id}'")
        self._users[user.user_id] = user

    def update(self, user):
        """Updates a user in memory.

        Args:
            user: User instance to update.
            
        Raises:
            UserNotFoundError: If the user is not found.
        """
        if user.user_id not in self._users:
            raise UserNotFoundError(f"No existe ningún usuario con ID '{user.user_id}'")
        self._users[user.user_id] = user

    def get(self, user_id):
        """Retrieves a user by its ID.

        Args:
            user_id: Unique identifier of the user.

        Returns:
            The user instance if found.

        Raises:
            UserNotFoundError: If no user with the given ID exists.
        """
        user = self._users.get(user_id)
        if user is None:
            raise UserNotFoundError(
                f"No existe ningún usuario con ID '{user_id}'"
            )
        return user

    def list(self):
        """Retrieves all stored users.

        Returns:
            A list of all user instances.
        """
        return list(self._users.values())

    def delete(self, user_id):
        """Deletes a user by its ID if it exists.

        Args:
            user_id: Unique identifier of the user to delete.
        """
        self._users.pop(user_id, None)

# domain/user_repository.py

from domain.user import User


class UserRepository:
    """Abstract repository interface for User instances.

    This repository defines the contract for persisting, retrieving,
    listing, and deleting user entities. Concrete implementations
    must provide the actual data storage logic.

    Methods:
        save: Stores or updates a user.
        get: Retrieves a user by its identifier.
        list: Retrieves all stored users.
        delete: Removes a user by its identifier.
    """

    def save(self, user: User):
        """Stores or updates a user.

        Args:
            user: User instance to persist.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def get(self, user_id: str) -> User | None:
        """Retrieves a user by its identifier.

        Args:
            user_id: Unique identifier of the user.

        Returns:
            The user instance if found, otherwise None.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def list(self) -> list[User]:
        """Retrieves all stored users.

        Returns:
            A list containing all users.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def delete(self, user_id: str):
        """Deletes a user by its identifier.

        Args:
            user_id: Unique identifier of the user to delete.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

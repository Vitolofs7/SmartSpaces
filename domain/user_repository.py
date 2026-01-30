# domain/user_repository.py

from domain.user import User


class UserRepository:
    """Abstract repository interface for managing User instances."""

    def save(self, user: User):
        """Saves a user instance to the repository.

        Args:
            user: The User instance to save.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def get(self, user_id: str) -> User | None:
        """Retrieves a user by their unique ID.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            The User instance if found, or None otherwise.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def list(self) -> list[User]:
        """Returns all users stored in the repository.

        Returns:
            A list of all User instances.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def delete(self, user_id: str):
        """Deletes a user by their ID.

        Args:
            user_id: The ID of the user to delete.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

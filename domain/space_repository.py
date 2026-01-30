# domain/space_repository.py

from domain.space import Space


class SpaceRepository:
    """Abstract repository interface for managing Space instances."""

    def save(self, space: Space):
        """Saves a space instance to the repository.

        Args:
            space: The Space instance to save.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def get(self, space_id: str) -> Space | None:
        """Retrieves a space by its unique ID.

        Args:
            space_id: The ID of the space to retrieve.

        Returns:
            The Space instance if found, or None otherwise.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def list(self) -> list[Space]:
        """Returns all spaces stored in the repository.

        Returns:
            A list of all Space instances.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def delete(self, space_id: str):
        """Deletes a space by its ID.

        Args:
            space_id: The ID of the space to delete.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

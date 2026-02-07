# domain/space_repository.py

from domain.space import Space


class SpaceRepository:
    """Abstract repository interface for Space instances.

    This repository defines the contract for persisting, retrieving,
    listing, and deleting space entities. Concrete implementations
    must provide the actual data storage logic.

    Methods:
        save: Stores or updates a space.
        get: Retrieves a space by its identifier.
        list: Retrieves all stored spaces.
        delete: Removes a space by its identifier.
    """

    def save(self, space: Space):
        """Stores or updates a space.

        Args:
            space: Space instance to persist.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def get(self, space_id: str) -> Space | None:
        """Retrieves a space by its identifier.

        Args:
            space_id: Unique identifier of the space.

        Returns:
            The space instance if found, otherwise None.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def list(self) -> list[Space]:
        """Retrieves all stored spaces.

        Returns:
            A list containing all spaces.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def delete(self, space_id: str):
        """Deletes a space by its identifier.

        Args:
            space_id: Unique identifier of the space to delete.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

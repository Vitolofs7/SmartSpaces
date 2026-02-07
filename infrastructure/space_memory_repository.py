# infrastructure/space_memory_repository.py

from domain.space_repository import SpaceRepository


class SpaceMemoryRepository(SpaceRepository):
    """In-memory implementation of the SpaceRepository interface.

    Stores spaces in a dictionary using their IDs as keys. Useful for testing
    or scenarios without a persistent storage backend.
    """

    def __init__(self):
        """Initializes an empty in-memory space repository."""
        self._data = {}

    def save(self, space):
        """Stores or updates a space in memory.

        Args:
            space: Space instance to save.
        """
        self._data[space.space_id] = space

    def get(self, space_id):
        """Retrieves a space by its ID.

        Args:
            space_id: Unique identifier of the space.

        Returns:
            The space instance if found, otherwise None.
        """
        return self._data.get(space_id)

    def list(self):
        """Retrieves all stored spaces.

        Returns:
            A list of all space instances.
        """
        return list(self._data.values())

    def delete(self, space_id):
        """Deletes a space by its ID if it exists.

        Args:
            space_id: Unique identifier of the space to delete.
        """
        self._data.pop(space_id, None)

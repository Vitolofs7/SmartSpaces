# infrastructure/space_memory_repository.py

from domain.space_repository import SpaceRepository


class SpaceMemoryRepository(SpaceRepository):
    """In-memory implementation of the SpaceRepository interface."""

    def __init__(self):
        """Initializes an empty in-memory data store for spaces."""
        self._data = {}

    def save(self, space):
        """Saves a space in memory.

        Args:
            space: The Space instance to save.
        """
        self._data[space.space_id] = space

    def get(self, space_id):
        """Retrieves a space by its ID.

        Args:
            space_id: The ID of the space to retrieve.

        Returns:
            The Space instance if found, or None otherwise.
        """
        return self._data.get(space_id)

    def list(self):
        """Returns all spaces stored in memory.

        Returns:
            A list of all Space instances.
        """
        return list(self._data.values())

    def delete(self, space_id):
        """Deletes a space from memory by its ID.

        Args:
            space_id: The ID of the space to delete.
        """
        self._data.pop(space_id, None)

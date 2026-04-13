"""infrastructure/space_memory_repository.py"""

from domain.space_repository import SpaceRepository
from domain.exceptions import (
    SpaceAlreadyExistsException,
    SpaceNotFoundError,
)


class SpaceMemoryRepository(SpaceRepository):
    """In-memory implementation of the SpaceRepository interface.

    Stores spaces in a dictionary using their IDs as keys. Assigns unique
    auto-incremented IDs to new spaces. Useful for testing or scenarios
    without a persistent storage backend.
    """

    def __init__(self):
        """Initializes an empty in-memory space repository with auto-increment ID tracking."""
        self._spaces = {}
        self._last_id = 0

    def save(self, space):
        """Stores or updates a space in memory.

        If the space does not have an ID, assigns a new unique ID.

        Args:
            space: Space instance to save.

        Raises:
            SpaceAlreadyExistsException: If saving a new space whose ID already exists.
        """
        if space.space_id is None:
            self._last_id += 1
            space._space_id = f"S{self._last_id}"
        elif space.space_id in self._spaces:
            raise SpaceAlreadyExistsException(f"Ya existe un espacio con ID '{space.space_id}'")
        self._spaces[space.space_id] = space

    def update(self, space):
        """Updates a space in memory.

        Args:
            space: Space instance to update.

        Raises:
            SpaceNotFoundError: If space is not found.
        """
        if space.space_id not in self._spaces:
            raise SpaceNotFoundError(f"No existe ningún espacio con ID '{space.space_id}'")
        self._spaces[space.space_id] = space

    def get(self, space_id):
        """Retrieves a space by its ID.

        Args:
            space_id: Unique identifier of the space.

        Returns:
            The space instance if found.

        Raises:
            SpaceNotFoundError: If no space with the given ID exists.
        """
        space = self._spaces.get(space_id)
        if space is None:
            raise SpaceNotFoundError(
                f"No existe ningún espacio con ID '{space_id}'"
            )
        return space

    def list(self):
        """Retrieves all stored spaces.

        Returns:
            A list of all space instances.
        """
        return list(self._spaces.values())

    def delete(self, space_id):
        """Deletes a space by its ID if it exists.

        Args:
            space_id: Unique identifier of the space to delete.
        """
        self._spaces.pop(space_id, None)

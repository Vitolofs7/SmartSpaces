"""infrastructure/space_memory_repository.py"""

from domain.space_repository import SpaceRepository
from infrastructure.errors import SpaceAlreadyExistsError


class SpaceMemoryRepository(SpaceRepository):
    """In-memory implementation of the SpaceRepository interface.

    Stores spaces in a dictionary using their IDs as keys. Assigns unique
    auto-incremented IDs to new spaces. Checks for duplicates to support
    error handling in the menu.
    """

    def __init__(self):
        """Initializes an empty in-memory space repository with auto-increment ID tracking."""
        self._spaces = {}
        self._last_id = 0

    def save(self, space):
        """Stores or updates a space in memory.

        Raises:
            SpaceAlreadyExistsError: If a space with the same ID or name already exists.
        """
        # Check for duplicates by ID
        if space.space_id is not None and space.space_id in self._spaces:
            raise SpaceAlreadyExistsError(f"A space with ID '{space.space_id}' already exists")

        # Check for duplicates by name
        for s in self._spaces.values():
            if s.space_name.lower() == space.space_name.lower():
                raise SpaceAlreadyExistsError(f"A space with name '{space.space_name}' already exists")

        # Assign a new ID if necessary
        if space.space_id is None:
            self._last_id += 1
            space._space_id = f"S{self._last_id}"

        self._spaces[space.space_id] = space

    def get(self, space_id):
        """Retrieves a space by its ID."""
        return self._spaces.get(space_id)

    def list(self):
        """Retrieves all stored spaces."""
        return list(self._spaces.values())

    def delete(self, space_id):
        """Deletes a space by its ID if it exists."""
        self._spaces.pop(space_id, None)
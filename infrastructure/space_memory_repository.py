# infrastructure/space_memory_repository.py

from domain.space_repository import SpaceRepository


class SpaceMemoryRepository(SpaceRepository):
    def __init__(self):
        self._data = {}

    def save(self, space):
        self._data[space.space_id] = space

    def get(self, space_id):
        return self._data.get(space_id)

    def list(self):
        return list(self._data.values())

    def delete(self, space_id):
        self._data.pop(space_id, None)

# domain/space_repository.py

from domain.space import Space


class SpaceRepository:
    def save(self, space: Space):
        raise NotImplementedError

    def get(self, space_id: str) -> Space | None:
        raise NotImplementedError

    def list(self) -> list[Space]:
        raise NotImplementedError

    def delete(self, space_id: str):
        raise NotImplementedError

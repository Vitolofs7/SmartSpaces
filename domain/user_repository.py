from domain.user import User


class UserRepository:
    """Abstract interface for managing User instances."""

    def save(self, user: User): raise NotImplementedError

    def get(self, user_id: str) -> User | None: raise NotImplementedError

    def list(self) -> list[User]: raise NotImplementedError

    def delete(self, user_id: str): raise NotImplementedError

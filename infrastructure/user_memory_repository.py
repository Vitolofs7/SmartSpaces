from domain.user_repository import UserRepository


class UserMemoryRepository(UserRepository):
    def __init__(self): self._data = {}

    def save(self, user): self._data[user.user_id] = user

    def get(self, user_id): return self._data.get(user_id)

    def list(self): return list(self._data.values())

    def delete(self, user_id): self._data.pop(user_id, None)

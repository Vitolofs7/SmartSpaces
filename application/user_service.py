# application/user_service.py

class UserService:
    def __init__(self, user_repository):
        self._user_repository = user_repository

    def list_users(self):
        return self._user_repository.list()

# application/user_service.py

class UserService:
    """Application service responsible for managing users.

    This service provides user-related operations and acts as an abstraction
    layer between the application logic and the user repository.

    Args:
        user_repository: Repository responsible for storing and retrieving users.
    """

    def __init__(self, user_repository):
        """Initializes the user service with its repository.

        Args:
            user_repository: Repository used to manage user persistence.
        """
        self._user_repository = user_repository

    def list_users(self):
        """Retrieves all stored users.

        Returns:
            A list containing all users.
        """
        return self._user_repository.list()

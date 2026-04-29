"""application/user_service.py"""
from domain.user import User
from domain.exceptions import UserNotFoundError, UserAlreadyExistsException


class UserService:
    """Application service responsible for managing users.

    This service provides user-related operations and acts as an abstraction
    layer between the application logic and the user repository.

    Args:
        user_repo: Repository responsible for storing and retrieving users.
    """

    def __init__(self, user_repo):
        """Initializes the user service with its repository.

        Args:
            user_repo: Repository used to manage user persistence.
        """
        self._user_repo = user_repo

    def list_users(self):
        """Retrieves all stored users.

        Returns:
            A list containing all users.
        """
        return self._user_repo.list()

    def get_user(self, user_id: str):
        """Recupera un usuario por su ID.

        Raises:
            UserNotFoundError: Si no existe el usuario.
        """
        return self._user_repo.get(user_id)


    def create_user(self, user_id: str, name: str, surname1: str, surname2: str):
        """Crea un nuevo usuario.

        Args:
            user_id: Identificador único (ej: "U1")
            name: Nombre de pila
            surname1: Primer apellido
            surname2: Segundo apellido

        Returns:
            El usuario creado

        Raises:
            UserAlreadyExistsException: Si el ID ya existe
            ValueError: Si algún campo está vacío
        """
        user = User(user_id, name, surname1, surname2)
        self._user_repo.save(user)
        return user


    def deactivate_user(self, user_id: str):
        """Desactiva un usuario existente.

        Args:
            user_id: ID del usuario a desactivar

        Returns:
            El usuario desactivado

        Raises:
            UserNotFoundError: Si no existe el usuario
        """
        user = self._user_repo.get(user_id)
        user.deactivate()
        self._user_repo.update(user)
        return user

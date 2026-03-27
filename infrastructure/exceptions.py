"""infrastructure/exceptions.py

Excepciones personalizadas del dominio para errores de persistencia.
Transforma errores de SQLite en conceptos que el dominio entiende.
"""


class RepositoryException(Exception):
    """Excepción base para todos los errores de persistencia."""
    pass


class SpaceAlreadyExistsException(RepositoryException):
    """Se lanza cuando se intenta guardar un espacio con un ID ya existente."""
    pass


class SpaceNotFoundError(RepositoryException):
    """Se lanza cuando se busca un espacio que no existe en la base de datos."""
    pass


class UserAlreadyExistsException(RepositoryException):
    """Se lanza cuando se intenta guardar un usuario con un ID ya existente."""
    pass


class UserNotFoundError(RepositoryException):
    """Se lanza cuando se busca un usuario que no existe en la base de datos."""
    pass


class BookingAlreadyExistsException(RepositoryException):
    """Se lanza cuando se intenta crear una reserva con un ID ya existente."""
    pass


class BookingNotFoundError(RepositoryException):
    """Se lanza cuando se busca una reserva que no existe."""
    pass


class PersistenceException(RepositoryException):
    """Se lanza ante cualquier otro error inesperado del motor de base de datos."""
    pass
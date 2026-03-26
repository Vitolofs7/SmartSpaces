class RepositoryError(Exception):
    """Excepción base para todos los errores de persistencia del repositorio de espacios."""
    pass


class SpaceAlreadyExistsError(RepositoryError):
    """Se lanza cuando se intenta guardar un espacio con un ID que ya existe en la base de datos."""
    pass


class SpaceNotFoundError(RepositoryError):
    """Se lanza cuando se busca un espacio que no existe en la base de datos."""
    pass


class PersistenceError(RepositoryError):
    """Se lanza ante cualquier otro error inesperado del motor de base de datos."""
    pass
"""infrastructure/user_sqlite_repository.py

Repositorio SQLite para persistencia de usuarios basado en el dominio real.
"""

import sqlite3
from domain.user import User
from infrastructure.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundError,
    PersistenceException,
)


class UserSQLiteRepository:
    """Repositorio SQLite para persistencia de usuarios."""

    def __init__(self, db_path: str = "smartspaces.db"):
        self._db_path = db_path

    def save(self, user: User) -> None:
        """Persiste un usuario en la base de datos."""
        conn = sqlite3.connect(self._db_path)
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (user_id, name, surname1, surname2)
                    VALUES (?, ?, ?, ?)
                """, (user.user_id, user.name, user.surname1, user.surname2))
        except sqlite3.IntegrityError:
            raise UserAlreadyExistsException(
                f"Ya existe un usuario con ID '{user.user_id}'"
            )
        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al guardar el usuario: {e}")
        finally:
            conn.close()

    def get(self, user_id: str) -> User:
        """Recupera un usuario por su ID."""
        conn = sqlite3.connect(self._db_path)
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, name, surname1, surname2
                FROM users WHERE user_id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            if row is None:
                raise UserNotFoundError(
                    f"No existe ningún usuario con ID '{user_id}'"
                )
            
            user_id, name, surname1, surname2 = row
            return User(user_id, name, surname1, surname2)
            
        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al leer el usuario: {e}")
        finally:
            conn.close()

    def list(self) -> list[User]:
        """Recupera todos los usuarios."""
        conn = sqlite3.connect(self._db_path)
        usuarios = []
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, name, surname1, surname2 FROM users")
            
            for user_id, name, surname1, surname2 in cursor.fetchall():
                usuarios.append(User(user_id, name, surname1, surname2))
            
            return usuarios
        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al listar usuarios: {e}")
        finally:
            conn.close()

    def update(self, user: User) -> None:
        """Actualiza los datos de un usuario."""
        conn = sqlite3.connect(self._db_path)
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users
                    SET name = ?, surname1 = ?, surname2 = ?
                    WHERE user_id = ?
                """, (user.name, user.surname1, user.surname2, user.user_id))
        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al actualizar el usuario: {e}")
        finally:
            conn.close()

    def delete(self, user_id: str) -> None:
        """Elimina un usuario de la base de datos."""
        conn = sqlite3.connect(self._db_path)
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al eliminar el usuario: {e}")
        finally:
            conn.close()
import sqlite3
from domain.space import Space
from domain.space_meetingroom import SpaceMeetingRoom
from infrastructure.errors import (
    SpaceAlreadyExistsError,
    SpaceNotFoundError,
    PersistenceError,
)


class RepositorioSpacesSQLite:
    """Repositorio de espacios usando SQLite.

    Gestiona la persistencia de objetos Space y SpaceMeetingRoom en una
    base de datos SQLite, con métodos para crear, obtener, actualizar,
    listar y eliminar espacios.

    Attributes:
        _ruta_bd: Ruta del archivo de la base de datos SQLite.
    """

    def __init__(self, ruta_bd: str = "smartspaces.db"):
        """Inicializa el repositorio con la ruta de la base de datos.

        Args:
            ruta_bd: Ruta del archivo SQLite.
        """
        self._ruta_bd = ruta_bd

    def save(self, space: Space) -> None:
        """Guarda un nuevo espacio en la base de datos.

        Si el espacio ya existe (por ID), lanza SpaceAlreadyExistsError.
        Maneja espacios genéricos y salas de reuniones.

        Args:
            space: Instancia de Space o SpaceMeetingRoom a guardar.

        Raises:
            SpaceAlreadyExistsError: Si ya existe un espacio con ese ID.
            PersistenceError: Si ocurre un error de SQLite.
        """
        conn = sqlite3.connect(self._ruta_bd)
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA foreign_keys = ON")
                # Insert en tabla principal de spaces
                cursor.execute(
                    "INSERT INTO spaces VALUES (?, ?, ?, ?, ?)",
                    (
                        space.space_id,
                        space.space_name,
                        space.capacity,
                        space.space_type,
                        space.space_status,
                    ),
                )

                # Si es una sala de reuniones, insert en meeting_rooms
                if isinstance(space, SpaceMeetingRoom):
                    cursor.execute(
                        "INSERT INTO meeting_rooms VALUES (?, ?, ?, ?, ?)",
                        (
                            space.space_id,
                            space.room_number,
                            space.floor,
                            space.equipment_list,
                            space.num_power_outlets,
                        ),
                    )

        except sqlite3.IntegrityError:
            raise SpaceAlreadyExistsError(
                f"A space with an id already exists '{space.space_id}'"
            )
        except sqlite3.OperationalError as e:
            raise PersistenceError(f"Error saving space: {e}")
        finally:
            conn.close()

    def give(self, space_id: str) -> Space:
        """Obtiene un espacio por su ID.

        Args:
            space_id: ID del espacio a recuperar.

        Returns:
            Instancia de Space o SpaceMeetingRoom.

        Raises:
            SpaceNotFoundError: Si no existe el espacio.
            PersistenceError: Si ocurre un error de SQLite.
        """
        conn = sqlite3.connect(self._ruta_bd)
        try:
            cursor = conn.cursor()
            # Consulta la tabla principal
            cursor.execute("SELECT * FROM spaces WHERE space_id = ?", (space_id,))
            row = cursor.fetchone()
            if row is None:
                raise SpaceNotFoundError(f"There is no space with ID '{space_id}'")

            space_id, name, capacity, type, status = row

            # Consulta la tabla de meeting_rooms
            cursor.execute(
                "SELECT * FROM meeting_rooms WHERE space_id = ?", (space_id,)
            )
            meeting_room = cursor.fetchone()

            if meeting_room:
                _, room_number, floor, equipment_list, num_power_outlets = meeting_room
                space = SpaceMeetingRoom(
                    space_id,
                    name,
                    capacity,
                    room_number,
                    floor,
                    equipment_list,
                    num_power_outlets,
                )
                space.space_status = status
                return space

            # Si no es sala de reuniones, devuelve Space normal
            space = Space(space_id, name, capacity, type)
            space.space_status = status
            return space

        except sqlite3.OperationalError as e:
            raise PersistenceError(f"Error reading space: {e}")
        finally:
            conn.close()

    def update(self, space: Space) -> None:
        """Actualiza un espacio existente en la base de datos.

        Args:
            space: Instancia de Space o SpaceMeetingRoom con los nuevos datos.

        Raises:
            PersistenceError: Si ocurre un error de SQLite.
        """
        conn = sqlite3.connect(self._ruta_bd)
        try:
            with conn:
                cursor = conn.cursor()
                # Actualiza tabla principal
                cursor.execute(
                    """
                    UPDATE spaces
                    SET space_name = ?, capacity = ?, space_type = ?, space_status = ?
                    WHERE space_id = ?
                    """,
                    (
                        space.space_name,
                        space.capacity,
                        space.space_type,
                        space.space_status,
                        space.space_id,
                    ),
                )

                # Si es sala de reuniones, actualiza tabla meeting_rooms
                if isinstance(space, SpaceMeetingRoom):
                    cursor.execute(
                        """
                        UPDATE meeting_rooms
                        SET room_number = ?, floor = ?, equipment_list = ?, num_power_outlets = ?
                        WHERE space_id = ?
                        """,
                        (
                            space.room_number,
                            space.floor,
                            space.equipment_list,
                            space.num_power_outlets,
                            space.space_id,
                        ),
                    )

        except sqlite3.OperationalError as e:
            raise PersistenceError(f"Error updating space: {e}")
        finally:
            conn.close()

    def list(self) -> list[Space]:
        """Lista todos los espacios en la base de datos.

        Returns:
            Lista de instancias de Space o SpaceMeetingRoom.

        Raises:
            PersistenceError: Si ocurre un error de SQLite.
        """
        conn = sqlite3.connect(self._ruta_bd)
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM spaces")
            spaces_rows = cursor.fetchall()

            spaces = []
            for row in spaces_rows:
                space_id, name, capacity, type, status = row
                # Revisa si es sala de reuniones
                cursor.execute(
                    "SELECT * FROM meeting_rooms WHERE space_id = ?", (space_id,)
                )
                meeting_room = cursor.fetchone()
                if meeting_room:
                    _, room_number, floor, equipment_list, num_power_outlets = meeting_room
                    space = SpaceMeetingRoom(
                        space_id,
                        name,
                        capacity,
                        room_number,
                        floor,
                        equipment_list,
                        num_power_outlets,
                    )
                else:
                    space = Space(space_id, name, capacity, type)
                space.space_status = status
                spaces.append(space)
            return spaces
        except sqlite3.OperationalError as e:
            raise PersistenceError(f"Error listing spaces: {e}")
        finally:
            conn.close()

    def delete(self, space_id: str) -> None:
        """Elimina un espacio por su ID.

        Args:
            space_id: ID del espacio a eliminar.

        Raises:
            PersistenceError: Si ocurre un error de SQLite.
        """
        conn = sqlite3.connect(self._ruta_bd)
        try:
            with conn:
                cursor = conn.cursor()
                # Primero elimina la sala de reuniones si existe
                cursor.execute("DELETE FROM meeting_rooms WHERE space_id = ?", (space_id,))
                # Luego elimina el espacio principal
                cursor.execute("DELETE FROM spaces WHERE space_id = ?", (space_id,))
        except sqlite3.OperationalError as e:
            raise PersistenceError(f"Error deleting space: {e}")
        finally:
            conn.close()
"""infrastructure/space_sqlite_repository.py

Repositorio SQLite para persistencia de espacios (Space y SpaceMeetingRoom).
Transforma excepciones sqlite3 en excepciones de dominio.
"""

import sqlite3
from domain.space import Space
from domain.space_meetingroom import SpaceMeetingRoom
from infrastructure.exceptions import (
    SpaceAlreadyExistsException,
    SpaceNotFoundError,
    PersistenceException,
)


class SpaceSQLiteRepository:
    def __init__(self, db_path: str = "smartspaces.db"):
        self._db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self._db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def save(self, space: Space) -> None:
        conn = self._connect()
        try:
            with conn:
                cursor = conn.cursor()

                # Asignar ID automático si es None
                if space.space_id is None:
                    cursor.execute("SELECT MAX(CAST(SUBSTR(space_id,2) AS INTEGER)) FROM spaces")
                    max_id = cursor.fetchone()[0] or 0
                    space.space_id = f"S{max_id + 1}"

                cursor.execute(
                    """
                    INSERT INTO spaces
                    (space_id, space_name, capacity, space_type, space_status)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        space.space_id,
                        space.space_name,
                        space.capacity,
                        space.space_type,
                        space.space_status,
                    ),
                )

                if isinstance(space, SpaceMeetingRoom):
                    equipment_str = ",".join(space.equipment_list)
                    cursor.execute(
                        """
                        INSERT INTO meeting_rooms
                        (space_id, room_number, floor, equipment_list, num_power_outlets)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (
                            space.space_id,
                            space.room_number,
                            space.floor,
                            equipment_str,
                            space.num_power_outlets,
                        ),
                    )

        except sqlite3.IntegrityError:
            raise SpaceAlreadyExistsException(
                f"Ya existe un espacio con ID '{space.space_id}'"
            )
        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al guardar el espacio: {e}")
        finally:
            conn.close()

    def get(self, space_id: str) -> Space:
        conn = self._connect()
        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT space_id, space_name, capacity, space_type, space_status
                FROM spaces WHERE space_id = ?
                """,
                (space_id,),
            )

            row = cursor.fetchone()
            if row is None:
                raise SpaceNotFoundError(
                    f"No existe ningún espacio con ID '{space_id}'"
                )

            sid, space_name, capacity, space_type, space_status = row

            cursor.execute(
                """
                SELECT room_number, floor, equipment_list, num_power_outlets
                FROM meeting_rooms WHERE space_id = ?
                """,
                (sid,),
            )

            mr_row = cursor.fetchone()
            if mr_row:
                room_number, floor, equipment_str, num_power_outlets = mr_row
                equipment_list = equipment_str.split(",") if equipment_str else []
                obj = SpaceMeetingRoom(
                    space_id=sid,
                    space_name=space_name,
                    capacity=capacity,
                    room_number=room_number,
                    floor=floor,
                    equipment_list=equipment_list,
                    num_power_outlets=num_power_outlets,
                )
            else:
                obj = Space(
                    space_id=sid,
                    space_name=space_name,
                    capacity=capacity,
                    space_type=space_type,
                )

            obj._space_status = space_status
            return obj

        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al leer el espacio: {e}")
        finally:
            conn.close()

    def list(self) -> list:
        conn = self._connect()
        espacios = []

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT 
                    s.space_id,
                    s.space_name,
                    s.capacity,
                    s.space_type,
                    s.space_status,
                    mr.room_number,
                    mr.floor,
                    mr.equipment_list,
                    mr.num_power_outlets
                FROM spaces s
                LEFT JOIN meeting_rooms mr 
                    ON s.space_id = mr.space_id
                """
            )

            for row in cursor.fetchall():
                (
                    sid,
                    space_name,
                    capacity,
                    space_type,
                    space_status,
                    room_number,
                    floor,
                    equipment_str,
                    num_power_outlets,
                ) = row

                if room_number is not None:
                    equipment_list = (
                        equipment_str.split(",") if equipment_str else []
                    )
                    obj = SpaceMeetingRoom(
                        space_id=sid,
                        space_name=space_name,
                        capacity=capacity,
                        room_number=room_number,
                        floor=floor,
                        equipment_list=equipment_list,
                        num_power_outlets=num_power_outlets,
                    )
                else:
                    obj = Space(
                        space_id=sid,
                        space_name=space_name,
                        capacity=capacity,
                        space_type=space_type,
                    )

                obj._space_status = space_status
                espacios.append(obj)

            return espacios

        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al listar espacios: {e}")
        finally:
            conn.close()

    def update(self, space: Space) -> None:
        conn = self._connect()
        try:
            with conn:
                cursor = conn.cursor()

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

                if isinstance(space, SpaceMeetingRoom):
                    equipment_str = ",".join(space.equipment_list)
                    cursor.execute(
                        """
                        UPDATE meeting_rooms
                        SET room_number = ?, floor = ?, equipment_list = ?, num_power_outlets = ?
                        WHERE space_id = ?
                        """,
                        (
                            space.room_number,
                            space.floor,
                            equipment_str,
                            space.num_power_outlets,
                            space.space_id,
                        ),
                    )

        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al actualizar el espacio: {e}")
        finally:
            conn.close()

    def delete(self, space_id: str) -> None:
        conn = self._connect()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM spaces WHERE space_id = ?",
                    (space_id,),
                )

        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al eliminar el espacio: {e}")
        finally:
            conn.close()
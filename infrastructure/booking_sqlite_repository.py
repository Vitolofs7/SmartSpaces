"""infrastructure/booking_sqlite_repository.py

Repositorio SQLite para persistencia de reservas.
"""

import sqlite3
from datetime import datetime
from domain.booking import Booking
from domain.user import User
from domain.space import Space
from domain.space_meetingroom import SpaceMeetingRoom
from domain.booking_repository import BookingRepository
from domain.exceptions import (
    BookingAlreadyExistsException,
    BookingNotFoundError,
    PersistenceException,
)


class BookingSQLiteRepository(BookingRepository):
    """Repositorio SQLite para persistencia de reservas."""

    def __init__(self, db_path: str = "smartspaces.db"):
        self._db_path = db_path

    def _connect(self):
        conn = sqlite3.connect(self._db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def save(self, booking: Booking) -> None:
        """Persiste una reserva en la base de datos."""
        conn = self._connect()
        try:
            with conn:
                cursor = conn.cursor()
                if booking.booking_id is None:
                    cursor.execute("SELECT MAX(CAST(SUBSTR(booking_id,2) AS INTEGER)) FROM bookings")
                    max_id = cursor.fetchone()[0] or 0
                    booking._booking_id = f"B{max_id + 1}"
                    
                cursor.execute("""
                    INSERT INTO bookings 
                    (booking_id, user_id, space_id, start_time, end_time, booking_status)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    booking.booking_id,
                    booking.user.user_id,
                    booking.space.space_id,
                    booking.start_time.isoformat(),
                    booking.end_time.isoformat(),
                    booking.status
                ))
        except sqlite3.IntegrityError:
            raise BookingAlreadyExistsException(f"Ya existe una reserva con ID '{booking.booking_id}'")
        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al guardar la reserva: {e}")
        finally:
            conn.close()

    def update(self, booking: Booking) -> None:
        """Actualiza una reserva existente en la base de datos."""
        conn = self._connect()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE bookings 
                    SET user_id = ?, space_id = ?, start_time = ?, end_time = ?, booking_status = ?
                    WHERE booking_id = ?
                """, (
                    booking.user.user_id,
                    booking.space.space_id,
                    booking.start_time.isoformat(),
                    booking.end_time.isoformat(),
                    booking.status,
                    booking.booking_id
                ))
                if cursor.rowcount == 0:
                    raise BookingNotFoundError(f"No existe ninguna reserva con ID '{booking.booking_id}'")
        except BookingNotFoundError:
            raise
        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al actualizar la reserva: {e}")
        finally:
            conn.close()

    def get(self, booking_id: str) -> Booking:
        """Recupera una reserva por su ID y reconstruye la entidad Booking."""
        conn = self._connect()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    b.booking_id, b.start_time, b.end_time, b.booking_status,
                    u.user_id, u.name, u.surname1, u.surname2, u.active,
                    s.space_id, s.space_name, s.capacity, s.space_type, s.space_status,
                    mr.room_number, mr.floor, mr.equipment_list, mr.num_power_outlets
                FROM bookings b
                JOIN users u ON b.user_id = u.user_id
                JOIN spaces s ON b.space_id = s.space_id
                LEFT JOIN meeting_rooms mr ON s.space_id = mr.space_id
                WHERE b.booking_id = ?
            """, (booking_id,))
            
            row = cursor.fetchone()
            if row is None:
                raise BookingNotFoundError(
                    f"No existe ninguna reserva con ID '{booking_id}'"
                )
            
            (bid, start_time, end_time, booking_status,
             user_id, name, surname1, surname2, active,
             space_id, space_name, capacity, space_type, space_status,
             room_number, floor, equipment_str, num_power_outlets) = row

            user = User(user_id, name, surname1, surname2)
            if not active:
                user.deactivate()

            if room_number is not None:
                equipment_list = equipment_str.split(",") if equipment_str else []
                space = SpaceMeetingRoom(
                    space_id=space_id,
                    space_name=space_name,
                    capacity=capacity,
                    room_number=room_number,
                    floor=floor,
                    equipment_list=equipment_list,
                    num_power_outlets=num_power_outlets,
                )
            else:
                space = Space(space_id, space_name, capacity, space_type)
            space._space_status = space_status

            booking = Booking(space, user,
                            datetime.fromisoformat(start_time),
                            datetime.fromisoformat(end_time))
            booking._booking_id = bid
            booking._booking_status = booking_status
            return booking

        except BookingNotFoundError:
            raise
        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al leer la reserva: {e}")
        finally:
            conn.close()

    def delete(self, booking_id: str) -> None:
        """Elimina una reserva de la base de datos."""
        conn = self._connect()
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM bookings WHERE booking_id = ?", (booking_id,))
        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al eliminar la reserva: {e}")
        finally:
            conn.close()

    def list(self) -> list[Booking]:
        """Recupera todas las reservas usando JOINs para reconstruir entidades."""
        conn = self._connect()
        reservas = []
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    b.booking_id, b.start_time, b.end_time, b.booking_status,
                    u.user_id, u.name, u.surname1, u.surname2, u.active,
                    s.space_id, s.space_name, s.capacity, s.space_type, s.space_status,
                    mr.room_number, mr.floor, mr.equipment_list, mr.num_power_outlets
                FROM bookings b
                JOIN users u ON b.user_id = u.user_id
                JOIN spaces s ON b.space_id = s.space_id
                LEFT JOIN meeting_rooms mr ON s.space_id = mr.space_id
            """)

            for row in cursor.fetchall():
                (bid, start_time, end_time, booking_status,
                 user_id, name, surname1, surname2, active,
                 space_id, space_name, capacity, space_type, space_status,
                 room_number, floor, equipment_str, num_power_outlets) = row

                user = User(user_id, name, surname1, surname2)
                if not active:
                    user.deactivate()

                if room_number is not None:
                    equipment_list = equipment_str.split(",") if equipment_str else []
                    space = SpaceMeetingRoom(
                        space_id=space_id,
                        space_name=space_name,
                        capacity=capacity,
                        room_number=room_number,
                        floor=floor,
                        equipment_list=equipment_list,
                        num_power_outlets=num_power_outlets,
                    )
                else:
                    space = Space(space_id, space_name, capacity, space_type)
                space._space_status = space_status

                booking = Booking(space, user,
                                datetime.fromisoformat(start_time),
                                datetime.fromisoformat(end_time))
                booking._booking_id = bid
                booking._booking_status = booking_status
                reservas.append(booking)

            return reservas
        except sqlite3.OperationalError as e:
            raise PersistenceException(f"Error al listar reservas: {e}")
        finally:
            conn.close()
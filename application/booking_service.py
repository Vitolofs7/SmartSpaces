# application/booking_service.py
from domain.booking import Booking
from domain.space import Space
from domain.user import User
from datetime import datetime


class BookingService:

    def __init__(self, booking_repo, space_repo, user_repo):
        self._booking_repo = booking_repo
        self._space_repo = space_repo
        self._user_repo = user_repo

    def create_booking(self, user_name, space_name, start_time, end_time):
        # Buscar usuario por nombre
        user = next(
            (u for u in self._user_repo.list() if u.full_name() == user_name),
            None
        )
        if not user:
            raise ValueError("User not found")

        # Buscar espacio por nombre
        space = next(
            (s for s in self._space_repo.list() if s.space_name == space_name),
            None
        )
        if not space:
            raise ValueError("Space not found")

        # Validar solapamientos antes de crear booking
        self._check_overlap(space, start_time, end_time)

        # Crear booking usando la instancia concreta del repositorio
        booking = Booking.create(
            space=space,
            user=user,
            start_time=start_time,
            end_time=end_time,
            booking_repo=self._booking_repo
        )

        # Guardar booking y actualizar espacio
        self._booking_repo.save(booking)
        self._space_repo.save(space)

        return booking

    def cancel_booking(self, booking_id: str):
        booking = self._booking_repo.get(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if not booking.is_active():
            raise ValueError("Only active bookings can be cancelled")

        booking.cancel()
        booking.space.release()

        self._space_repo.save(booking.space)
        self._booking_repo.save(booking)

    def finish_booking(self, booking_id: str):
        booking = self._booking_repo.get(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if not booking.is_active():
            raise ValueError("Only active bookings can be finished")

        booking.finish()
        booking.space.release()

        self._space_repo.save(booking.space)
        self._booking_repo.save(booking)

    def list_bookings(self):
        return self._booking_repo.list()

    def get_booking(self, booking_id: str):
        return self._booking_repo.get(booking_id)

    def get_bookings_for_user(self, user_name: str):
        user = self._find_user_by_name(user_name)
        if not user:
            return []
        return [b for b in self._booking_repo.list() if b.user.user_id == user.user_id]

    def get_bookings_for_space(self, space_name: str):
        space = self._find_space_by_name(space_name)
        if not space:
            return []
        return [b for b in self._booking_repo.list() if b.space.space_id == space.space_id]

    # =========================
    # Métodos auxiliares
    # =========================

    def _find_user_by_name(self, full_name: str):
        for u in self._user_repo.list():
            if u.full_name().lower() == full_name.lower():
                return u
        return None

    def _find_space_by_name(self, space_name: str):
        for s in self._space_repo.list():
            if s.space_name.lower() == space_name.lower():
                return s
        return None

    def _check_overlap(self, space: Space, start_time: datetime, end_time: datetime):
        bookings_for_space = [
            b for b in self._booking_repo.list()
            if b.space.space_id == space.space_id and b.is_active()
        ]
        for b in bookings_for_space:
            if start_time < b.end_time and b.start_time < end_time:
                raise ValueError(
                    f"Space '{space.space_name}' is already booked "
                    f"from {b.start_time} to {b.end_time}"
                )

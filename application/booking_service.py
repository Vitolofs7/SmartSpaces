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

    def create_booking(self, booking_id: str, user_id: str, space_id: str, start_time: datetime,
                       end_time: datetime) -> Booking:
        user: User | None = self._user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")
        if not user.is_active():
            raise ValueError("User is inactive")

        space: Space | None = self._space_repo.get(space_id)
        if not space:
            raise ValueError("Space not found")
        if not space.is_available():
            raise ValueError("Space is not available for booking")

        booking = Booking(booking_id, space, user, start_time, end_time)

        space.reserve()
        self._space_repo.save(space)

        self._booking_repo.save(booking)

        return booking

    def cancel_booking(self, booking_id: str):
        booking: Booking | None = self._booking_repo.get(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if not booking.is_active():
            raise ValueError("Only active bookings can be cancelled")

        booking.cancel()
        booking._space.release()
        self._space_repo.save(booking._space)
        self._booking_repo.save(booking)

    def finish_booking(self, booking_id: str):
        booking: Booking | None = self._booking_repo.get(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        if not booking.is_active():
            raise ValueError("Only active bookings can be finished")

        booking.finish()
        booking._space.release()
        self._space_repo.save(booking._space)
        self._booking_repo.save(booking)

    def get_booking(self, booking_id: str) -> Booking | None:
        return self._booking_repo.get(booking_id)

    def list_bookings(self) -> list[Booking]:
        return self._booking_repo.list()

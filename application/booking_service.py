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

    """
       Creates a booking for a user in a specific space between start_time and end_time.
       Validates that the user and space exist and are available.
    """

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

        self._check_overlap(space, start_time, end_time)

        booking = Booking(booking_id, space, user, start_time, end_time)

        space.reserve()
        self._space_repo.save(space)

        self._booking_repo.save(booking)

        return booking

    """
       Cancels an active booking.
       Releases the associated space and updates the booking status.
    """

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

    """
        Marks an active booking as finished.
        Releases the associated space and updates the booking status.
    """

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

    """
        Returns the booking with the given ID, or None if it does not exist.
    """

    def get_booking(self, booking_id: str) -> Booking | None:
        return self._booking_repo.get(booking_id)

    """
        Returns all bookings in the repository.
    """

    def list_bookings(self) -> list[Booking]:
        return self._booking_repo.list()

    """
        Returns all bookings associated with a specific user.
    """

    def get_bookings_for_user(self, user_id: str) -> list[Booking]:
        return [b for b in self._booking_repo.list() if b._user.user_id == user_id]

    """
        Returns all bookings associated with a specific space.
    """

    def get_bookings_for_space(self, space_id: str) -> list[Booking]:
        return [b for b in self._booking_repo.list() if b._space.space_id == space_id]

    """
            Checks if the given space has any active bookings that overlap with the specified time range.
            Raises ValueError if an overlap is found.
    """

    def _check_overlap(self, space: Space, start_time: datetime, end_time: datetime):
        bookings_for_space = [
            b for b in self._booking_repo.list()
            if b._space.space_id == space.space_id and b.is_active()
        ]
        for b in bookings_for_space:
            if start_time < b._end_time and b._start_time < end_time:
                raise ValueError(
                    f"Space '{space.space_name}' is already booked from {b._start_time} to {b._end_time}."
                )

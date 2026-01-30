# application/booking_service.py
from domain.booking import Booking
from domain.space import Space
from domain.user import User
from datetime import datetime


class BookingService:
    def __init__(self, booking_repo, space_repo, user_repo):
        """Initializes the booking service with the necessary repositories.

            Args:
                booking_repo: Repository to manage bookings.
                space_repo: Repository to manage spaces.
                user_repo: Repository to manage users.
        """
        self._booking_repo = booking_repo
        self._space_repo = space_repo
        self._user_repo = user_repo

    def create_booking(self, booking_id: str, user_id: str, space_id: str, start_time: datetime,
                       end_time: datetime) -> Booking:
        """Creates a booking for a user in a specific space between two times.

        Validates that the user and space exist and are available, and checks
        for overlapping active bookings.

        Args:
            booking_id: Unique identifier for the booking.
            user_id: Identifier of the user making the booking.
            space_id: Identifier of the space to be booked.
            start_time: Start datetime of the booking.
            end_time: End datetime of the booking.

        Returns:
            The created Booking instance.

        Raises:
            ValueError: If the user does not exist or is inactive, the space does not exist
                        or is unavailable, or if there is an overlapping booking.
        """
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

    def cancel_booking(self, booking_id: str):
        """Cancels an active booking.

        Releases the associated space and updates the booking status.

        Args:
            booking_id: Identifier of the booking to cancel.

        Raises:
            ValueError: If the booking does not exist or is not active.
        """
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
        """Marks an active booking as finished.

        Releases the associated space and updates the booking status.

        Args:
            booking_id: Identifier of the booking to finish.

        Raises:
            ValueError: If the booking does not exist or is not active.
        """
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
        """Retrieves a booking by its ID.

        Args:
            booking_id: Identifier of the booking.

        Returns:
            The Booking instance if it exists, or None otherwise.
        """
        return self._booking_repo.get(booking_id)

    def list_bookings(self) -> list[Booking]:
        """Returns all bookings stored in the repository.

        Returns:
            List of all Booking instances.
        """
        return self._booking_repo.list()

    def get_bookings_for_user(self, user_id: str) -> list[Booking]:
        """Returns all bookings associated with a specific user.

        Args:
            user_id: Identifier of the user.

        Returns:
            List of bookings belonging to the user.
        """
        return [b for b in self._booking_repo.list() if b._user.user_id == user_id]

    def get_bookings_for_space(self, space_id: str) -> list[Booking]:
        """Returns all bookings associated with a specific space.

        Args:
            space_id: Identifier of the space.

        Returns:
            List of bookings for the given space.
        """
        return [b for b in self._booking_repo.list() if b._space.space_id == space_id]

    def _check_overlap(self, space: Space, start_time: datetime, end_time: datetime):
        """Checks if the given space has any active bookings that overlap with a specified time range.

        Args:
            space: Space to check.
            start_time: Start of the time range.
            end_time: End of the time range.

        Raises:
            ValueError: If there is any active booking overlapping with the given time range.
        """
        bookings_for_space = [
            b for b in self._booking_repo.list()
            if b._space.space_id == space.space_id and b.is_active()
        ]
        for b in bookings_for_space:
            if start_time < b._end_time and b._start_time < end_time:
                raise ValueError(
                    f"Space '{space.space_name}' is already booked from {b._start_time} to {b._end_time}."
                )

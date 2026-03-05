# application/booking_service.py

from domain.booking import Booking
from domain.space import Space
from datetime import datetime


class BookingService:
    """Application service responsible for managing space bookings.

    This service coordinates the creation, modification, cancellation, completion,
    and retrieval of bookings, ensuring business rules are enforced such as:
    user and space existence, space availability, and booking overlap validation.

    Args:
        booking_repo: Repository responsible for storing and retrieving bookings.
        space_repo: Repository responsible for storing and retrieving spaces.
        user_repo: Repository responsible for storing and retrieving users.
    """

    def __init__(self, booking_repo, space_repo, user_repo):
        """Initializes the booking service with its repositories.

        Args:
            booking_repo: Repository used to manage booking persistence.
            space_repo: Repository used to manage space persistence.
            user_repo: Repository used to manage user persistence.
        """
        self._booking_repo, self._space_repo, self._user_repo = booking_repo, space_repo, user_repo

    def create_booking(self, user_name, space_name, start_time, end_time):
        """Creates a new booking for a user in a specific space and time range.

        Validates that the user and space exist and ensures that the requested
        time slot does not overlap with other active bookings for the same space.

        Args:
            user_name: Full name of the user making the booking.
            space_name: Name of the space to be booked.
            start_time: Booking start datetime.
            end_time: Booking end datetime.

        Returns:
            The newly created booking instance.

        Raises:
            ValueError: If the user or space does not exist.
            ValueError: If the booking time overlaps with an existing active booking.
        """
        user = next((user for user in self._user_repo.list() if user.full_name() == user_name), None)
        if not user: raise ValueError("User not found")
        space = next((space for space in self._space_repo.list() if space.space_name == space_name), None)
        if not space: raise ValueError("Space not found")
        self._check_overlap(space, start_time, end_time)
        booking = Booking.create(space=space, user=user, start_time=start_time, end_time=end_time,
                                 booking_repo=self._booking_repo)
        self._booking_repo.save(booking)
        self._space_repo.save(space)
        return booking

    def modify_booking(self, booking_id: str, new_start, new_end):
        """Modifies the schedule of an existing booking.

        Args:
            booking_id: Unique identifier of the booking to modify.
            new_start: New booking start datetime.
            new_end: New booking end datetime.

        Returns:
            The updated booking instance.

        Raises:
            ValueError: If the booking does not exist.
        """
        booking = self._booking_repo.get(booking_id)
        if not booking:
            raise ValueError("Booking not found")
        booking.reschedule(new_start, new_end, self._booking_repo)
        self._booking_repo.save(booking)
        return booking

    def cancel_booking(self, booking_id: str):
        """Cancels an active booking and releases the associated space.

        Args:
            booking_id: Unique identifier of the booking to cancel.

        Raises:
            ValueError: If the booking does not exist.
            ValueError: If the booking is not active.
        """
        booking = self._booking_repo.get(booking_id)
        if not booking: raise ValueError("Booking not found")
        if not booking.is_active(): raise ValueError("Only active bookings can be cancelled")
        booking.cancel()
        booking.space.release()
        self._space_repo.save(booking.space)
        self._booking_repo.save(booking)

    def finish_booking(self, booking_id: str):
        """Marks an active booking as finished and releases the associated space.

        Args:
            booking_id: Unique identifier of the booking to finish.

        Raises:
            ValueError: If the booking does not exist.
            ValueError: If the booking is not active.
        """
        booking = self._booking_repo.get(booking_id)
        if not booking: raise ValueError("Booking not found")
        if not booking.is_active(): raise ValueError("Only active bookings can be finished")
        booking.finish()
        booking.space.release()
        self._space_repo.save(booking.space)
        self._booking_repo.save(booking)

    def list_bookings(self):
        """Returns all stored bookings.

        Returns:
            A list containing all bookings.
        """
        return self._booking_repo.list()

    def get_booking(self, booking_id: str):
        """Retrieves a booking by its identifier.

        Args:
            booking_id: Unique identifier of the booking.

        Returns:
            The booking instance if found, otherwise None.
        """
        return self._booking_repo.get(booking_id)

    def get_bookings_for_user(self, user_name: str):
        """Retrieves all bookings associated with a specific user.

        Args:
            user_name: Full name of the user.

        Returns:
            A list of bookings belonging to the user. Returns an empty list if the user is not found.
        """
        user = self._find_user_by_name(user_name)
        return [booking for booking in self._booking_repo.list() if booking.user.user_id == user.user_id] if user else []

    def get_bookings_for_space(self, space_name: str):
        """Retrieves all bookings associated with a specific space.

        Args:
            space_name: Name of the space.

        Returns:
            A list of bookings for the space. Returns an empty list if the space is not found.
        """
        space = self._find_space_by_name(space_name)
        return [booking for booking in self._booking_repo.list() if booking.space.space_id == space.space_id] if space else []

    def get_available_spaces(self, start_time: datetime, end_time: datetime):
        """Retrieves all spaces available for a given time range.

        Args:
            start_time: Desired booking start datetime.
            end_time: Desired booking end datetime.

        Returns:
            A list of spaces that are not booked during the specified time range.
        """
        all_spaces = self._space_repo.list()
        bookings = self._booking_repo.list()

        available_spaces = []
        for space in all_spaces:
            overlapping = any(
                booking.is_active() and booking.space.space_id == space.space_id and
                start_time < booking.end_time and booking.start_time < end_time
                for booking in bookings
            )
            if not overlapping:
                available_spaces.append(space)

        return available_spaces

    def _find_user_by_name(self, full_name: str):
        """Finds a user by full name

        Args:
            full_name: Full name of the user.

        Returns:
            The user instance if found, otherwise None.
        """
        return next((user for user in self._user_repo.list() if user.full_name().lower() == full_name.lower()), None)

    def _find_space_by_name(self, space_name: str):
        """Finds a space by name

        Args:
            space_name: Name of the space.

        Returns:
            The space instance if found, otherwise None.
        """
        return next((space for space in self._space_repo.list() if space.space_name.lower() == space_name.lower()), None)

    def _check_overlap(self, space: Space, start_time: datetime, end_time: datetime):
        """Validates that a booking time range does not overlap with existing active bookings.

        Args:
            space: Space to validate availability for.
            start_time: Proposed booking start datetime.
            end_time: Proposed booking end datetime.

        Raises:
            ValueError: If an active booking overlaps with the requested time range.
        """
        for booking in (booking for booking in self._booking_repo.list() if booking.space.space_id == space.space_id and booking.is_active()):
            if start_time < booking.end_time and booking.start_time < end_time:
                raise ValueError(f"Space '{space.space_name}' is already booked from {booking.start_time} to {booking.end_time}")

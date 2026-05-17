"""application/booking_service.py"""

from domain import booking
from domain.booking import Booking
from datetime import datetime
from domain.exceptions import BookingNotFoundError, BookingConflictError


class BookingService:
    """Application service responsible for managing space bookings.

    This service coordinates the creation, modification, cancellation, completion,
    and retrieval of bookings, ensuring business rules are enforced such as:
    user and space existence, user booking limits, and space availability.
    Overlap validation is delegated entirely to the domain layer.

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
        self._booking_repo, self._space_repo, self._user_repo = (
            booking_repo,
            space_repo,
            user_repo,
        )

    def create_booking(self, user_name, space_name, start_time, end_time):
        """Creates a new booking for a user in a specific space and time range.

        Validates that the user and space exist, that the user has not exceeded
        their active booking limit, and that the requested duration does not exceed
        the user's maximum booking duration. Overlap and availability checks are
        delegated to the domain layer via Booking.create.

        Args:
            user_name: Full name of the user making the booking.
            space_name: Name of the space to be booked.
            start_time: Booking start datetime.
            end_time: Booking end datetime.

        Returns:
            The newly created booking instance.

        Raises:
            ValueError: If the user or space does not exist.
            ValueError: If the user has reached their maximum active bookings limit.
            ValueError: If the requested duration exceeds the user's maximum booking duration.
            ValueError: If the booking time overlaps with an existing active booking.
        """
        user = next(
            (user for user in self._user_repo.list() if user.full_name() == user_name),
            None,
        )
        if not user:
            raise ValueError("User not found")
        space = next(
            (
                space
                for space in self._space_repo.list()
                if space.space_name == space_name
            ),
            None,
        )
        if not space:
            raise ValueError("Space not found")

        active_user_bookings = [
            booking
            for booking in self._booking_repo.list()
            if booking.user.user_id == user.user_id and booking.is_active()
        ]
        if len(active_user_bookings) >= user.max_active_bookings:
            raise BookingConflictError(
                f"User '{user_name}' has reached the maximum of {user.max_active_bookings} active booking(s)."
            )

        duration = end_time - start_time
        if duration > user.max_booking_duration:
            raise ValueError(
                f"Booking duration exceeds the allowed maximum of {user.max_booking_duration} for user '{user_name}'."
            )

        booking = Booking.create(
            space=space,
            user=user,
            start_time=start_time,
            end_time=end_time,
            booking_repo=self._booking_repo,
        )
        self._booking_repo.save(booking)

        space.reserve()
        self._space_repo.update(space)

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
        booking.reschedule(new_start, new_end, self._booking_repo)
        self._booking_repo.update(booking)
        return booking

    def cancel_booking(self, booking_id: str):
        """Cancels an active booking and releases the associated space.

        The domain method booking.cancel() handles the space state transition
        internally; the service only needs to persist the booking.

        Args:
            booking_id: Unique identifier of the booking to cancel.

        Raises:
            ValueError: If the booking does not exist.
            ValueError: If the booking is not active.
        """
        try:
            booking = self._booking_repo.get(booking_id)
        except BookingNotFoundError:
            raise ValueError("Booking not found")
        if not booking.is_active():
            raise ValueError("Only active bookings can be cancelled")
        booking.cancel()
        self._booking_repo.update(booking)
        return booking

    def finish_booking(self, booking_id: str):
        """Marks an active booking as finished and releases the associated space.

        The domain method booking.finish() handles the space state transition
        internally; the service only needs to persist the booking.

        Args:
            booking_id: Unique identifier of the booking to finish.

        Raises:
            ValueError: If the booking does not exist.
            ValueError: If the booking is not active.
        """
        try:
            booking = self._booking_repo.get(booking_id)
        except BookingNotFoundError:
            raise ValueError("Booking not found")
        if not booking.is_active():
            raise ValueError("Only active bookings can be finished")
        booking.finish()
        self._booking_repo.update(booking)
        return booking

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
        try:
            return self._booking_repo.get(booking_id)
        except BookingNotFoundError:
            return None

    def get_bookings_for_user(self, user_name: str):
        """Retrieves all bookings associated with a specific user.

        Args:
            user_name: Full name of the user.

        Returns:
            A list of bookings belonging to the user. Returns an empty list if the user is not found.
        """
        user = self._find_user_by_name(user_name)
        return (
            [
                booking
                for booking in self._booking_repo.list()
                if booking.user.user_id == user.user_id
            ]
            if user
            else []
        )

    def get_bookings_for_space(self, space_name: str):
        """Retrieves all bookings associated with a specific space.

        Args:
            space_name: Name of the space.

        Returns:
            A list of bookings for the space. Returns an empty list if the space is not found.
        """
        space = self._find_space_by_name(space_name)
        return (
            [
                booking
                for booking in self._booking_repo.list()
                if booking.space.space_id == space.space_id
            ]
            if space
            else []
        )

    def get_available_spaces(self, start_time: datetime, end_time: datetime):
        """Retrieves all spaces available for a given time range.

        Args:
            start_time: Desired booking start datetime.
            end_time: Desired booking end datetime.

        Returns:
            A list of spaces that are not booked during the specified time range.
        """
        available_spaces = []
        for space in self._space_repo.list():
            overlapping = any(
                booking.is_active()
                and booking.space.space_id == space.space_id
                and start_time < booking.end_time
                and booking.start_time < end_time
                for booking in self._booking_repo.list()
            )
            if not overlapping:
                available_spaces.append(space)
        return available_spaces

    def _find_user_by_name(self, full_name: str):
        """Finds a user by full name.

        Args:
            full_name: Full name of the user.

        Returns:
            The user instance if found, otherwise None.
        """
        return next(
            (
                user
                for user in self._user_repo.list()
                if user.full_name().lower() == full_name.lower()
            ),
            None,
        )

    def _find_space_by_name(self, space_name: str):
        """Finds a space by name.

        Args:
            space_name: Name of the space.

        Returns:
            The space instance if found, otherwise None.
        """
        return next(
            (
                space
                for space in self._space_repo.list()
                if space.space_name.lower() == space_name.lower()
            ),
            None,
        )

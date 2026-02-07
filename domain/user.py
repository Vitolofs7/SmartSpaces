# domain/user.py

from datetime import timedelta


class User:
    """Domain entity representing a user who can make bookings.

    A user has identification, full name, and account status. The entity
    also defines booking-related constraints such as maximum active
    bookings and maximum booking duration.

    Attributes:
        _active: Indicates whether the user is active.
        _max_active_bookings: Maximum number of concurrent active bookings allowed.
        _max_booking_duration: Maximum allowed duration for a single booking.
    """

    def __init__(self, user_id, name, surname1, surname2):
        """Initializes a user instance.

        Args:
            user_id: Unique identifier of the user.
            name: First name of the user.
            surname1: First surname of the user.
            surname2: Second surname of the user.

        Raises:
            ValueError: If any of the user fields are empty.
        """
        user_id, name, surname1, surname2 = (x.strip() for x in
                                             (user_id or "", name or "", surname1 or "", surname2 or ""))
        if not all([user_id, name, surname1, surname2]):
            raise ValueError("All user fields must be non-empty.")
        self.__user_id, self._name, self._surname1, self._surname2 = user_id, name, surname1, surname2
        self._active = True
        self._max_active_bookings = 1
        self._max_booking_duration = timedelta(hours=2)

    @property
    def user_id(self):
        """Returns the unique identifier of the user."""
        return self.__user_id

    @property
    def name(self):
        """Returns the user's first name."""
        return self._name

    @property
    def surname1(self):
        """Returns the user's first surname."""
        return self._surname1

    @property
    def surname2(self):
        """Returns the user's second surname."""
        return self._surname2

    def full_name(self):
        """Returns the full name of the user.

        Returns:
            A string combining first name and surnames.
        """
        return f"{self.name} {self.surname1} {self.surname2}"

    def is_active(self):
        """Checks if the user is active.

        Returns:
            True if the user is active, otherwise False.
        """
        return self._active

    def deactivate(self):
        """Deactivates the user account."""
        self._active = False

    def can_make_booking(self):
        """Checks whether the user is allowed to make a booking.

        Returns:
            True if the user is active, otherwise False.
        """
        return self._active

    @property
    def max_active_bookings(self):
        """Returns the maximum number of active bookings the user can have."""
        return self._max_active_bookings

    @property
    def max_booking_duration(self):
        """Returns the maximum allowed duration for a single booking."""
        return self._max_booking_duration

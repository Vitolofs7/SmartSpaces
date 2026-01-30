from datetime import timedelta


class User:
    """Represents a user who can make bookings in the system."""

    def __init__(self, user_id, name, surname1, surname2):
        """Initializes a User instance with validation.

        Args:
            user_id: Unique identifier for the user.
            name: First name of the user.
            surname1: First surname of the user.
            surname2: Second surname of the user.

        Raises:
            ValueError: If any of the arguments are empty.
        """
        user_id = (user_id or "").strip()
        name = (name or "").strip()
        surname1 = (surname1 or "").strip()
        surname2 = (surname2 or "").strip()

        if not user_id:
            raise ValueError("User id cannot be empty.")
        if not name:
            raise ValueError("User name cannot be empty.")
        if not surname1:
            raise ValueError("User first surname cannot be empty")
        if not surname2:
            raise ValueError("User second surname cannot be empty")

        self.__user_id = user_id
        self._name = name
        self._surname1 = surname1
        self._surname2 = surname2
        self._active = True

        # Default rules (basic behaviour)
        self._max_active_bookings = 1
        self._max_booking_duration = timedelta(hours=2)

    @property
    def user_id(self):
        """Returns the unique identifier of the user."""
        return self.__user_id

    @property
    def name(self):
        """Returns the first name of the user."""
        return self._name

    @property
    def surname1(self):
        """Returns the first surname of the user."""
        return self._surname1

    @property
    def surname2(self):
        """Returns the second surname of the user."""
        return self._surname2

    def full_name(self):
        """Returns the full name of the user.

        Returns:
            Concatenation of name, surname1, and surname2.
        """
        return f"{self.name} {self.surname1} {self.surname2}"

    def is_active(self):
        """Checks if the user is currently active.

        Returns:
            True if the user is active, False otherwise.
        """
        return self._active

    def deactivate(self):
        """Deactivates the user, preventing future bookings."""
        self._active = False

    def can_make_booking(self):
        """Checks if the user is allowed to make bookings.

        Returns:
            True if the user is active, False otherwise.
        """
        return self._active

    @property
    def max_active_bookings(self):
        """Returns the maximum number of active bookings allowed for the user."""
        return self._max_active_bookings

    @property
    def max_booking_duration(self):
        """Returns the maximum duration allowed per booking for the user."""
        return self._max_booking_duration

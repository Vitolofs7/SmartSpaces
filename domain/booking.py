# domain/booking.py

class Booking:
    """Domain entity representing a booking for a space.

    A booking links a user with a space during a specific time range and
    maintains its lifecycle status (active, cancelled, or finished).
    It enforces business rules such as time validation, availability checks,
    and overlap prevention.

    Attributes:
        STATUS_ACTIVE: Indicates that the booking is currently active.
        STATUS_CANCELLED: Indicates that the booking has been cancelled.
        STATUS_FINISHED: Indicates that the booking has been completed.
    """

    STATUS_ACTIVE, STATUS_CANCELLED, STATUS_FINISHED = "ACTIVE", "CANCELLED", "FINISHED"
    _id_counter = 1

    def __init__(self, space, user, start_time, end_time):
        """Initializes a booking instance.

        Args:
            space: Space associated with the booking.
            user: User who owns the booking.
            start_time: Booking start datetime.
            end_time: Booking end datetime.

        Raises:
            ValueError: If start_time is not earlier than end_time.
        """
        if start_time >= end_time: raise ValueError("Start time must be before end time.")
        self._booking_id, self._space, self._user = None, space, user
        self._start_time, self._end_time = start_time, end_time
        self._booking_status = Booking.STATUS_ACTIVE

    @staticmethod
    def create(space, user, start_time, end_time, booking_repo):
        """Creates and validates a new booking.

        Ensures the user is active, the space is available, and that
        the new booking does not overlap with existing bookings.

        Args:
            space: Space to be booked.
            user: User requesting the booking.
            start_time: Booking start datetime.
            end_time: Booking end datetime.
            booking_repo: Repository used to validate existing bookings
                          and persist the new booking.

        Returns:
            The newly created booking instance.

        Raises:
            ValueError: If the user is inactive.
            ValueError: If the space is not available.
            ValueError: If the booking overlaps with an existing booking.
        """
        if not user.is_active(): raise ValueError("User is inactive")
        if not space.is_available(): raise ValueError("Space is not available")
        new_booking = Booking(space, user, start_time, end_time)
        for b in booking_repo.list():
            if b.space.space_id == space.space_id and new_booking.overlaps_with(b):
                raise ValueError(f"Space '{space.space_name}' already booked.")
        space.reserve()
        booking_repo.save(new_booking)
        return new_booking

    @property
    def booking_id(self):
        """Returns the unique identifier of the booking.

        Returns:
            Booking identifier.
        """
        return self._booking_id

    @property
    def space(self):
        """Returns the space associated with the booking.

        Returns:
            Space instance linked to the booking.
        """
        return self._space

    @property
    def user(self):
        """Returns the user associated with the booking.

        Returns:
            User instance linked to the booking.
        """
        return self._user

    @property
    def start_time(self):
        """Returns the booking start datetime.

        Returns:
            Start datetime of the booking.
        """
        return self._start_time

    @property
    def end_time(self):
        """Returns the booking end datetime.

        Returns:
            End datetime of the booking.
        """
        return self._end_time

    @property
    def status(self):
        """Returns the current booking status.

        Returns:
            Booking status string.
        """
        return self._booking_status

    def is_active(self):
        """Checks whether the booking is active.

        Returns:
            True if the booking is active, otherwise False.
        """
        return self._booking_status == Booking.STATUS_ACTIVE

    def cancel(self):
        """Cancels an active booking and releases the associated space.

        Raises:
            ValueError: If the booking is not active.
        """
        if not self.is_active(): raise ValueError("Only active bookings can be cancelled.")
        self._booking_status = Booking.STATUS_CANCELLED
        self._space.release()

    def finish(self):
        """Marks an active booking as finished and releases the associated space.

        Raises:
            ValueError: If the booking is not active.
        """
        if not self.is_active(): raise ValueError("Only active bookings can be finished.")
        self._booking_status = Booking.STATUS_FINISHED
        self._space.release()

    def overlaps_with(self, other):
        """Checks whether this booking overlaps with another booking.

        Args:
            other: Another booking instance to compare with.

        Returns:
            True if both bookings are active and overlap in time, otherwise False.
        """
        if not self.is_active() or not other.is_active(): return False
        return self._start_time < other.end_time and other.start_time < self._end_time

    def reschedule(self, new_start, new_end, booking_repo):
        """Reschedules the booking to a new time range.

        Ensures the booking remains valid and does not overlap with
        other active bookings for the same space.

        Args:
            new_start: New booking start datetime.
            new_end: New booking end datetime.
            booking_repo: Repository used to validate booking overlaps.

        Raises:
            ValueError: If the booking is not active.
            ValueError: If the new time range is invalid.
            ValueError: If the new time range overlaps with another booking.
        """
        if not self.is_active():
            raise ValueError("Only active bookings can be rescheduled.")
        if new_start >= new_end:
            raise ValueError("Start time must be before end time.")

        for b in booking_repo.list():
            if b.space.space_id == self.space.space_id and b != self and b.is_active():
                if new_start < b.end_time and b.start_time < new_end:
                    raise ValueError(
                        f"Space '{self.space.space_name}' is already booked from {b.start_time} to {b.end_time}")

        self._start_time = new_start
        self._end_time = new_end

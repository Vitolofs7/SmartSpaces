# domain/booking.py
from datetime import datetime


class Booking:
    """Represents a booking for a user in a specific space with a start and end time.

    Attributes:
        STATUS_ACTIVE: Status indicating the booking is active.
        STATUS_CANCELLED: Status indicating the booking was cancelled.
        STATUS_FINISHED: Status indicating the booking has finished.
    """

    STATUS_ACTIVE = "ACTIVE"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_FINISHED = "FINISHED"

    def __init__(self, booking_id, space, user, start_time, end_time):
        """Initializes a Booking instance.

        Validates that the booking_id is not empty and that start_time is
        before end_time.

        Args:
            booking_id: Unique identifier for the booking.
            space: The Space object being booked.
            user: The User object making the booking.
            start_time: Start datetime of the booking.
            end_time: End datetime of the booking.

        Raises:
            ValueError: If booking_id is empty or start_time is not before end_time.
        """
        if not booking_id:
            raise ValueError("Booking id cannot be empty.")
        if start_time >= end_time:
            raise ValueError("Start time must be before end time.")

        self.__booking_id = booking_id
        self._space = space
        self._user = user
        self._start_time = start_time
        self._end_time = end_time
        self._booking_status = Booking.STATUS_ACTIVE

    @property
    def booking_id(self):
        """Returns the unique identifier of the booking.

        Returns:
            The booking ID as a string.
        """
        return self.__booking_id

    @property
    def status(self):
        """Returns the current status of the booking.

        Returns:
            One of STATUS_ACTIVE, STATUS_CANCELLED, or STATUS_FINISHED.
        """
        return self._booking_status

    def is_active(self):
        """Checks if the booking is currently active.

        Returns:
            True if the booking is active, False otherwise.
        """
        return self._booking_status == Booking.STATUS_ACTIVE

    def cancel(self):
        """Cancels an active booking.

        Updates the booking status to STATUS_CANCELLED.

        Raises:
            ValueError: If the booking is not active.
        """
        if self._booking_status != Booking.STATUS_ACTIVE:
            raise ValueError("Only active bookings can be cancelled.")
        self._booking_status = Booking.STATUS_CANCELLED

    def finish(self):
        """Marks an active booking as finished.

        Updates the booking status to STATUS_FINISHED.

        Raises:
            ValueError: If the booking is not active.
        """
        if self._booking_status != Booking.STATUS_ACTIVE:
            raise ValueError("Only active bookings can be finished.")
        self._booking_status = Booking.STATUS_FINISHED

    def overlaps_with(self, other):
        """Checks if this booking overlaps with another booking.

        Only active bookings are considered. Two bookings overlap if their
        time ranges intersect.

        Args:
            other: Another Booking instance to compare against.

        Returns:
            True if the bookings overlap, False otherwise.
        """
        if not self.is_active() or not other.is_active():
            return False

        return (
                self._start_time < other._end_time
                and other._start_time < self._end_time
        )

    def duration(self):
        """Calculates the duration of the booking.

        Returns:
            A timedelta representing the length of the booking.
        """
        return self._end_time - self._start_time

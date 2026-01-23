# domain/booking.py
from datetime import datetime


class Booking:
    STATUS_ACTIVE = "ACTIVE"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_FINISHED = "FINISHED"

    def __init__(self, booking_id, space, user, start_time, end_time):
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

    # getters
    @property
    def booking_id(self):
        return self.__booking_id

    @property
    def status(self):
        return self._booking_status

    def is_active(self):
        return self._booking_status == Booking.STATUS_ACTIVE

    def cancel(self):
        if self._booking_status != Booking.STATUS_ACTIVE:
            raise ValueError("Only active bookings can be cancelled.")
        self._booking_status = Booking.STATUS_CANCELLED

    def finish(self):
        if self._booking_status != Booking.STATUS_ACTIVE:
            raise ValueError("Only active bookings can be finished.")
        self._booking_status = Booking.STATUS_FINISHED

    def overlaps_with(self, other):
        if not self.is_active() or not other.is_active():
            return False

        return (
                self._start_time < other._end_time
                and other._start_time < self._end_time
        )

    def duration(self):
        return self._end_time - self._start_time

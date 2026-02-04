from domain import booking_repository


class Booking:
    STATUS_ACTIVE, STATUS_CANCELLED, STATUS_FINISHED = "ACTIVE", "CANCELLED", "FINISHED"
    _id_counter = 1

    def __init__(self, space, user, start_time, end_time):
        if start_time >= end_time: raise ValueError("Start time must be before end time.")
        self._booking_id, self._space, self._user = None, space, user
        self._start_time, self._end_time = start_time, end_time
        self._booking_status = Booking.STATUS_ACTIVE

    @staticmethod
    def create(space, user, start_time, end_time, booking_repo):
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
        return self._booking_id

    @property
    def space(self):
        return self._space

    @property
    def user(self):
        return self._user

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def status(self):
        return self._booking_status

    def is_active(self):
        return self._booking_status == Booking.STATUS_ACTIVE

    def cancel(self):
        if not self.is_active(): raise ValueError("Only active bookings can be cancelled.")
        self._booking_status = Booking.STATUS_CANCELLED
        self._space.release()

    def finish(self):
        if not self.is_active(): raise ValueError("Only active bookings can be finished.")
        self._booking_status = Booking.STATUS_FINISHED
        self._space.release()

    def overlaps_with(self, other):
        if not self.is_active() or not other.is_active(): return False
        return self._start_time < other.end_time and other.start_time < self._end_time

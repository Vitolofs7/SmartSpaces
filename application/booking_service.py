from domain.booking import Booking
from domain.space import Space
from datetime import datetime


class BookingService:
    def __init__(self, booking_repo, space_repo, user_repo):
        self._booking_repo, self._space_repo, self._user_repo = booking_repo, space_repo, user_repo

    def create_booking(self, user_name, space_name, start_time, end_time):
        user = next((u for u in self._user_repo.list() if u.full_name() == user_name), None)
        if not user: raise ValueError("User not found")
        space = next((s for s in self._space_repo.list() if s.space_name == space_name), None)
        if not space: raise ValueError("Space not found")
        self._check_overlap(space, start_time, end_time)
        booking = Booking.create(space=space, user=user, start_time=start_time, end_time=end_time,
                                 booking_repo=self._booking_repo)
        self._booking_repo.save(booking)
        self._space_repo.save(space)
        return booking

    def cancel_booking(self, booking_id: str):
        b = self._booking_repo.get(booking_id)
        if not b: raise ValueError("Booking not found")
        if not b.is_active(): raise ValueError("Only active bookings can be cancelled")
        b.cancel();
        b.space.release()
        self._space_repo.save(b.space);
        self._booking_repo.save(b)

    def finish_booking(self, booking_id: str):
        b = self._booking_repo.get(booking_id)
        if not b: raise ValueError("Booking not found")
        if not b.is_active(): raise ValueError("Only active bookings can be finished")
        b.finish();
        b.space.release()
        self._space_repo.save(b.space);
        self._booking_repo.save(b)

    def list_bookings(self):
        return self._booking_repo.list()

    def get_booking(self, booking_id: str):
        return self._booking_repo.get(booking_id)

    def get_bookings_for_user(self, user_name: str):
        u = self._find_user_by_name(user_name)
        return [b for b in self._booking_repo.list() if b.user.user_id == u.user_id] if u else []

    def get_bookings_for_space(self, space_name: str):
        s = self._find_space_by_name(space_name)
        return [b for b in self._booking_repo.list() if b.space.space_id == s.space_id] if s else []

    # Aux
    def _find_user_by_name(self, full_name: str):
        return next((u for u in self._user_repo.list() if u.full_name().lower() == full_name.lower()), None)

    def _find_space_by_name(self, space_name: str):
        return next((s for s in self._space_repo.list() if s.space_name.lower() == space_name.lower()), None)

    def _check_overlap(self, space: Space, start_time: datetime, end_time: datetime):
        for b in (b for b in self._booking_repo.list() if b.space.space_id == space.space_id and b.is_active()):
            if start_time < b.end_time and b.start_time < end_time:
                raise ValueError(f"Space '{space.space_name}' is already booked from {b.start_time} to {b.end_time}")

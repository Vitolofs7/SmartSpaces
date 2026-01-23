# infrastructure/booking_memory_repository.py

from domain.booking_repository import BookingRepository


class BookingMemoryRepository(BookingRepository):
    def __init__(self):
        self._data = {}

    def save(self, booking):
        self._data[booking.booking_id] = booking

    def get(self, booking_id):
        return self._data.get(booking_id)

    def list(self):
        return list(self._data.values())

    def delete(self, booking_id):
        self._data.pop(booking_id, None)

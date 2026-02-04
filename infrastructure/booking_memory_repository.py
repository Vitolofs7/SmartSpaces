from domain.booking_repository import BookingRepository


class BookingMemoryRepository(BookingRepository):
    def __init__(self):
        self._data, self._last_id = {}, 0

    def save(self, booking):
        if booking.booking_id is None:
            self._last_id += 1
            booking._booking_id = f"B{self._last_id}"
        self._data[booking.booking_id] = booking

    def get(self, booking_id): return self._data.get(booking_id)

    def list(self): return list(self._data.values())

    def delete(self, booking_id): self._data.pop(booking_id, None)

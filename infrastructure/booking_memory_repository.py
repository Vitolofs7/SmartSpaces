# infrastructure/booking_memory_repository.py

from domain.booking_repository import BookingRepository


class BookingMemoryRepository(BookingRepository):
    """In-memory implementation of the BookingRepository interface."""

    def __init__(self):
        self._data = {}
        self._last_id = 0  # Nuevo atributo para controlar IDs

    def save(self, booking):
        """Saves a booking in memory, generating an ID if needed."""
        if booking.booking_id is None:
            self._last_id += 1
            booking._booking_id = f"B{self._last_id}"  # ID generado aquí
        self._data[booking.booking_id] = booking

    def get(self, booking_id):
        return self._data.get(booking_id)

    def list(self):
        return list(self._data.values())

    def delete(self, booking_id):
        self._data.pop(booking_id, None)

# infrastructure/booking_memory_repository.py

from domain.booking_repository import BookingRepository


class BookingMemoryRepository(BookingRepository):
    """In-memory implementation of the BookingRepository interface."""

    def __init__(self):
        """Initializes an empty in-memory data store for bookings."""
        self._data = {}

    def save(self, booking):
        """Saves a booking in memory.

        Args:
            booking: The Booking instance to save.
        """
        self._data[booking.booking_id] = booking

    def get(self, booking_id):
        """Retrieves a booking by its ID.

        Args:
            booking_id: The ID of the booking to retrieve.

        Returns:
            The Booking instance if found, or None otherwise.
        """
        return self._data.get(booking_id)

    def list(self):
        """Returns all bookings stored in memory.

        Returns:
            A list of all Booking instances.
        """
        return list(self._data.values())

    def delete(self, booking_id):
        """Deletes a booking from memory by its ID.

        Args:
            booking_id: The ID of the booking to delete.
        """
        self._data.pop(booking_id, None)

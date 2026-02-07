# infrastructure/booking_memory_repository.py

from domain.booking_repository import BookingRepository


class BookingMemoryRepository(BookingRepository):
    """In-memory implementation of the BookingRepository interface.

    Stores bookings in a dictionary and assigns unique IDs to new bookings.
    Suitable for testing or ephemeral data storage without a persistent database.
    """

    def __init__(self):
        """Initializes an empty in-memory repository with auto-increment ID tracking."""
        self._data, self._last_id = {}, 0

    def save(self, booking):
        """Stores or updates a booking in memory.

        If the booking does not have an ID, assigns a new unique ID.

        Args:
            booking: Booking instance to save.
        """
        if booking.booking_id is None:
            self._last_id += 1
            booking._booking_id = f"B{self._last_id}"
        self._data[booking.booking_id] = booking

    def get(self, booking_id):
        """Retrieves a booking by its ID.

        Args:
            booking_id: Unique identifier of the booking.

        Returns:
            The booking instance if found, otherwise None.
        """
        return self._data.get(booking_id)

    def list(self):
        """Retrieves all stored bookings.

        Returns:
            A list of all booking instances.
        """
        return list(self._data.values())

    def delete(self, booking_id):
        """Deletes a booking by its ID if it exists.

        Args:
            booking_id: Unique identifier of the booking to delete.
        """
        self._data.pop(booking_id, None)

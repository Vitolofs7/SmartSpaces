"""infrastructure/booking_memory_repository.py"""

from domain.booking_repository import BookingRepository
from domain.exceptions import (
    BookingAlreadyExistsException,
    BookingNotFoundError,
)


class BookingMemoryRepository(BookingRepository):
    """In-memory implementation of the BookingRepository interface.

    Stores bookings in a dictionary and assigns unique IDs to new bookings.
    Suitable for testing or ephemeral data storage without a persistent database.
    """

    def __init__(self):
        """Initializes an empty in-memory repository with auto-increment ID tracking."""
        self._bookings, self._last_id = {}, 0

    def save(self, booking):
        """Stores a new booking in memory.

        If the booking does not have an ID, assigns a new unique ID.

        Args:
            booking: Booking instance to save.
            
        Raises:
            BookingAlreadyExistsException: If the booking already exists.
        """
        if booking.booking_id is None:
            self._last_id += 1
            booking._booking_id = f"B{self._last_id}"
        elif booking.booking_id in self._bookings:
            raise BookingAlreadyExistsException(f"Ya existe una reserva con ID '{booking.booking_id}'")
        self._bookings[booking.booking_id] = booking

    def update(self, booking):
        """Updates a booking in memory.

        Args:
            booking: Booking instance to update.
            
        Raises:
            BookingNotFoundError: If the booking is not found.
        """
        if booking.booking_id not in self._bookings:
            raise BookingNotFoundError(f"No existe ninguna reserva con ID '{booking.booking_id}'")
        self._bookings[booking.booking_id] = booking

    def get(self, booking_id):
        """Retrieves a booking by its ID.

        Args:
            booking_id: Unique identifier of the booking.

        Returns:
            The booking instance if found.

        Raises:
            BookingNotFoundError: If no booking with the given ID exists.
        """
        booking = self._bookings.get(booking_id)
        if booking is None:
            raise BookingNotFoundError(
                f"No existe ninguna reserva con ID '{booking_id}'"
            )
        return booking

    def list(self):
        """Retrieves all stored bookings.

        Returns:
            A list of all booking instances.
        """
        return list(self._bookings.values())

    def delete(self, booking_id):
        """Deletes a booking by its ID if it exists.

        Args:
            booking_id: Unique identifier of the booking to delete.
        """
        self._bookings.pop(booking_id, None)

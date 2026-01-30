# domain/booking_repository.py

from domain.booking import Booking


class BookingRepository:
    """Abstract repository interface for managing Booking instances."""

    def save(self, booking: Booking):
        """Saves a booking instance to the repository.

        Args:
            booking: The Booking instance to save.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def get(self, booking_id: str) -> Booking | None:
        """Retrieves a booking by its unique ID.

        Args:
            booking_id: The ID of the booking to retrieve.

        Returns:
            The Booking instance if found, or None otherwise.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def list(self) -> list[Booking]:
        """Returns all bookings stored in the repository.

        Returns:
            A list of all Booking instances.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def delete(self, booking_id: str):
        """Deletes a booking by its ID.

        Args:
            booking_id: The ID of the booking to delete.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

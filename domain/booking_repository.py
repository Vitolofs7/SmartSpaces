# domain/booking_repository.py

from domain.booking import Booking


class BookingRepository:
    """Abstract repository interface for Booking instances.

    This repository defines the contract for persisting, retrieving,
    listing, and deleting booking entities. Concrete implementations
    must provide the actual data storage logic.

    Methods:
        save: Stores or updates a booking.
        get: Retrieves a booking by its identifier.
        list: Retrieves all stored bookings.
        delete: Removes a booking by its identifier.
    """

    def save(self, booking: Booking):
        """Stores or updates a booking.

        Args:
            booking: Booking instance to persist.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def get(self, booking_id: str) -> Booking | None:
        """Retrieves a booking by its identifier.

        Args:
            booking_id: Unique identifier of the booking.

        Returns:
            The booking instance if found, otherwise None.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def list(self) -> list[Booking]:
        """Retrieves all stored bookings.

        Returns:
            A list containing all bookings.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

    def delete(self, booking_id: str):
        """Deletes a booking by its identifier.

        Args:
            booking_id: Unique identifier of the booking to delete.

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError

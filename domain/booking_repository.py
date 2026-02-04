from domain.booking import Booking


class BookingRepository:
    """Abstract repository interface for Booking instances."""

    def save(self, booking: Booking): raise NotImplementedError

    def get(self, booking_id: str) -> Booking | None: raise NotImplementedError

    def list(self) -> list[Booking]: raise NotImplementedError

    def delete(self, booking_id: str): raise NotImplementedError

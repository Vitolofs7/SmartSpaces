"""domain/space.py"""


class Space:
    """Domain entity representing a reservable space.

    A space contains identification, capacity, type, and operational status.
    It manages its availability lifecycle including reservation, release,
    and maintenance state transitions.

    Availability for new bookings is determined exclusively by the absence of
    overlapping active bookings (enforced in Booking.create). The RESERVED status
    reflects that at least one active booking exists for the space, but does NOT
    block future non-overlapping bookings. Only MAINTENANCE acts as a global block.

    Attributes:
        STATUS_AVAILABLE: Indicates the space has no active bookings.
        STATUS_RESERVED: Indicates the space has at least one active booking.
        STATUS_MAINTENANCE: Indicates the space is unavailable due to maintenance.
        TYPE_GENERIC: Default type assigned to spaces when no type is provided.
    """

    STATUS_AVAILABLE = "AVAILABLE"
    STATUS_RESERVED = "RESERVED"
    STATUS_MAINTENANCE = "MAINTENANCE"
    TYPE_GENERIC = "Basic Space"

    def __init__(self, space_id, space_name, capacity, space_type=None):
        """Initializes a space instance.

        Args:
            space_id: Unique identifier of the space, or None for auto-assignment.
            space_name: Name of the space.
            capacity: Maximum number of occupants allowed.
            space_type: Optional classification of the space.

        Raises:
            ValueError: If space_name is empty.
            ValueError: If capacity is not greater than zero.
        """
        if space_id is not None and (not isinstance(space_id, str) or not space_id.strip()):
            raise ValueError("Space ID cannot be empty")
        space_name = (space_name or "").strip()
        if not space_name: raise ValueError("Space name cannot be empty")
        if capacity <= 0: raise ValueError("Capacity must be > 0")

        self.__space_id = space_id
        self.__space_name = space_name
        self.__capacity = capacity
        self._space_status = Space.STATUS_AVAILABLE
        self._space_type = space_type or Space.TYPE_GENERIC

    def __str__(self):
        """Returns a human-readable representation of the space.

        Returns:
            A formatted string describing the space.
        """
        return f"[{self.space_id}] {self.space_name}\n  • Type: {self.space_type}\n  • Status: {self.space_status}\n  • Capacity: {self.capacity}"

    @property
    def space_id(self):
        """Returns the unique identifier of the space."""
        return self.__space_id

    @space_id.setter
    def space_id(self, value):
        """Sets the unique identifier of the space."""
        self.__space_id = value

    @property
    def space_name(self):
        """Returns the name of the space."""
        return self.__space_name

    @space_name.setter
    def space_name(self, value):
        """Sets the name of the space."""
        self.__space_name = value

    @property
    def capacity(self):
        """Returns the capacity of the space."""
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        """Sets the capacity of the space.

        Raises:
            ValueError: If capacity is not greater than zero.
        """
        if value <= 0: raise ValueError("Capacity must be > 0")
        self.__capacity = value

    @property
    def space_status(self):
        """Returns the current status of the space."""
        return self._space_status

    @space_status.setter
    def space_status(self, value):
        """Sets the status of the space.

        Raises:
            ValueError: If the status value is invalid.
        """
        if value not in (Space.STATUS_AVAILABLE, Space.STATUS_RESERVED, Space.STATUS_MAINTENANCE):
            raise ValueError("Invalid status")
        self._space_status = value

    @property
    def space_type(self):
        """Returns the type of the space."""
        return self._space_type

    def is_available(self):
        """Checks whether the space has no active bookings.

        Returns:
            True if the space status is AVAILABLE, otherwise False.
        """
        return self._space_status == Space.STATUS_AVAILABLE

    def is_reserved(self):
        """Checks whether the space has at least one active booking.

        Returns:
            True if the space status is RESERVED, otherwise False.
        """
        return self._space_status == Space.STATUS_RESERVED

    def is_maintenance(self):
        """Checks whether the space is under maintenance.

        Returns:
            True if the space status is MAINTENANCE, otherwise False.
        """
        return self._space_status == Space.STATUS_MAINTENANCE

    def reserve(self):
        """Marks the space as reserved.

        Can be called on an AVAILABLE or already RESERVED space, since a space
        may have multiple non-overlapping bookings. Only blocked if under MAINTENANCE.

        Raises:
            ValueError: If the space is under maintenance.
        """
        if self._space_status == Space.STATUS_MAINTENANCE:
            raise ValueError("Space is under maintenance and cannot be reserved")
        self._space_status = Space.STATUS_RESERVED

    def release(self):
        """Releases the space and marks it as available.

        Raises:
            ValueError: If the space is not currently reserved.
        """
        if self._space_status != Space.STATUS_RESERVED:
            raise ValueError("Space not reserved")
        self._space_status = Space.STATUS_AVAILABLE

    def set_maintenance(self):
        """Sets the space status to maintenance mode."""
        self._space_status = Space.STATUS_MAINTENANCE

    def get_space_status_display(self):
        """Returns a human-readable representation of the space status.

        Returns:
            A formatted string describing the space status.
        """
        return {"AVAILABLE": "Available", "RESERVED": "Reserved", "MAINTENANCE": "Under Maintenance"}.get(
            self._space_status, "Unknown")

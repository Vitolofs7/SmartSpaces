# domain/space.py

class Space:
    """Domain entity representing a reservable space.

    A space contains identification, capacity, type, and operational status.
    It manages its availability lifecycle including reservation, release,
    and maintenance state transitions.

    Attributes:
        STATUS_AVAILABLE: Indicates the space is free to be reserved.
        STATUS_RESERVED: Indicates the space is currently reserved.
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
            space_id: Unique identifier of the space.
            space_name: Name of the space.
            capacity: Maximum number of occupants allowed.
            space_type: Optional classification of the space.

        Raises:
            ValueError: If space_id or space_name is empty.
            ValueError: If capacity is not greater than zero.
        """
        space_id, space_name = (space_id or "").strip(), (space_name or "").strip()
        if not space_id: raise ValueError("Space ID cannot be empty")
        if not space_name: raise ValueError("Space name cannot be empty")
        if capacity <= 0: raise ValueError("Capacity must be > 0")

        self.__space_id = space_id
        self.__space_name = space_name
        self.__capacity = capacity
        self._space_status = Space.STATUS_AVAILABLE
        self._space_type = space_type or Space.TYPE_GENERIC
        self._bookings = {}

    def __str__(self):
        """Returns a human-readable representation of the space.

        Returns:
            A formatted string describing the space.
        """
        return f"[{self.space_id}] {self.space_name}\n  • Type: {self.space_type}\n  • Status: {self.space_status}\n  • Capacity: {self.capacity}"

    @property
    def space_id(self):
        """Returns the unique identifier of the space.

        Returns:
            Space identifier.
        """
        return self.__space_id

    @space_id.setter
    def space_id(self, value):
        """Sets the unique identifier of the space.

        Args:
            value: New space identifier.
        """
        self.__space_id = value

    @property
    def space_name(self):
        """Returns the name of the space.

        Returns:
            Space name.
        """
        return self.__space_name

    @space_name.setter
    def space_name(self, value):
        """Sets the name of the space.

        Args:
            value: New space name.
        """
        self.__space_name = value

    @property
    def capacity(self):
        """Returns the capacity of the space.

        Returns:
            Maximum occupancy of the space.
        """
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        """Sets the capacity of the space.

        Args:
            value: New capacity value.

        Raises:
            ValueError: If capacity is not greater than zero.
        """
        if value <= 0: raise ValueError("Capacity must be > 0")
        self.__capacity = value

    @property
    def space_status(self):
        """Returns the current status of the space.

        Returns:
            Current space status.
        """
        return self._space_status

    @space_status.setter
    def space_status(self, value):
        """Sets the status of the space.

        Args:
            value: New status value.

        Raises:
            ValueError: If the status value is invalid.
        """
        if value not in (Space.STATUS_AVAILABLE, Space.STATUS_RESERVED, Space.STATUS_MAINTENANCE):
            raise ValueError("Invalid status")
        self._space_status = value

    @property
    def space_type(self):
        """Returns the type of the space.

        Returns:
            Space type classification.
        """
        return self._space_type

    def is_available(self):
        """Checks whether the space is available for reservation.

        Returns:
            True if the space is available, otherwise False.
        """
        return self._space_status == Space.STATUS_AVAILABLE

    def is_reserved(self):
        """Checks whether the space is currently reserved.

        Returns:
            True if the space is reserved, otherwise False.
        """
        return self._space_status == Space.STATUS_RESERVED

    def reserve(self):
        """Marks the space as reserved.

        Raises:
            ValueError: If the space is not currently available.
        """
        if self._space_status != Space.STATUS_AVAILABLE: raise ValueError("Space not available")
        self._space_status = Space.STATUS_RESERVED

    def release(self):
        """Releases the space and marks it as available.

        Raises:
            ValueError: If the space is not currently reserved.
        """
        if self._space_status != Space.STATUS_RESERVED: raise ValueError("Space not reserved")
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

# domain/space.py
class Space:
    """Represents a physical or virtual space that can be booked.

    Attributes:
        STATUS_AVAILABLE: Status indicating the space is available.
        STATUS_RESERVED: Status indicating the space is reserved.
        STATUS_MAINTENANCE: Status indicating the space is under maintenance.
        TYPE_GENERIC: Default type for a generic space.
    """

    STATUS_AVAILABLE = "AVAILABLE"
    STATUS_RESERVED = "RESERVED"
    STATUS_MAINTENANCE = "MAINTENANCE"
    TYPE_GENERIC = "Basic Space"

    def __init__(self, space_id, space_name, capacity, space_type=None):
        """Initializes a Space instance.

        Args:
            space_id: Unique identifier for the space.
            space_name: Name of the space.
            capacity: Maximum number of people the space can accommodate.
            space_type: Optional type of the space. Defaults to TYPE_GENERIC.

        Raises:
            ValueError: If space_id or space_name is empty, or capacity is <= 0.
        """
        space_id = (space_id or "").strip()
        space_name = (space_name or "").strip()

        if not space_id:
            raise ValueError("Space identifier cannot be empty.")
        if not space_name:
            raise ValueError("Space name cannot be empty.")
        if capacity <= 0:
            raise ValueError("Capacity must be greater than zero.")

        self.__space_id = space_id
        self.__space_name = space_name
        self.__capacity = capacity
        self._space_status = Space.STATUS_AVAILABLE
        self._space_type = space_type or Space.TYPE_GENERIC
        self._bookings = {}

    def __str__(self):
        """Returns a string representation of the space."""
        return (
            f"[{self.space_id}] {self.space_name}\n"
            f"  • Type: {self.space_type}\n"
            f"  • Status: {self.space_status}\n"
            f"  • Capacity: {self.capacity}"
        )

    @property
    def space_id(self):
        """Returns the unique identifier of the space."""
        return self.__space_id

    @property
    def space_name(self):
        """Returns the name of the space."""
        return self.__space_name

    @property
    def capacity(self):
        """Returns the maximum capacity of the space."""
        return self.__capacity

    @property
    def space_status(self):
        """Returns the current status of the space."""
        return self._space_status

    @property
    def space_type(self):
        """Returns the type of the space."""
        return self._space_type

    @space_id.setter
    def space_id(self, new_space_id):
        """Sets a new unique identifier for the space."""
        self.__space_id = new_space_id

    @space_name.setter
    def space_name(self, new_space_name):
        """Sets a new name for the space."""
        self.__space_name = new_space_name

    @capacity.setter
    def capacity(self, new_capacity):
        """Sets a new capacity for the space.

        Raises:
            ValueError: If the new capacity is less than or equal to zero.
        """
        if new_capacity <= 0:
            raise ValueError("Capacity must be greater than zero.")
        self.__capacity = new_capacity

    @space_status.setter
    def space_status(self, new_space_status):
        """Sets a new status for the space.

        Args:
            new_space_status: One of STATUS_AVAILABLE, STATUS_RESERVED, STATUS_MAINTENANCE.

        Raises:
            ValueError: If new_space_status is invalid.
        """
        if new_space_status not in (
                Space.STATUS_AVAILABLE,
                Space.STATUS_RESERVED,
                Space.STATUS_MAINTENANCE
        ):
            raise ValueError("Invalid space status.")
        self._space_status = new_space_status

    def is_available(self):
        """Checks if the space is available for booking.

        Returns:
            True if the space status is STATUS_AVAILABLE, False otherwise.
        """
        return self._space_status == Space.STATUS_AVAILABLE

    def is_reserved(self):
        """Checks if the space is currently reserved.

        Returns:
            True if the space status is STATUS_RESERVED, False otherwise.
        """
        return self._space_status == Space.STATUS_RESERVED

    def reserve(self):
        """Reserves the space if it is available.

        Raises:
            ValueError: If the space is under maintenance or not available.
        """
        if self._space_status == Space.STATUS_MAINTENANCE:
            raise ValueError("Cannot reserve a space under maintenance.")
        if self._space_status != Space.STATUS_AVAILABLE:
            raise ValueError("Space is not available for reservation.")
        self._space_status = Space.STATUS_RESERVED

    def release(self):
        """Releases a reserved space, making it available.

        Raises:
            ValueError: If the space is under maintenance or not reserved.
        """
        if self._space_status == Space.STATUS_MAINTENANCE:
            raise ValueError("Cannot release a space under maintenance.")
        if self._space_status != Space.STATUS_RESERVED:
            raise ValueError("Space is not reserved.")
        self._space_status = Space.STATUS_AVAILABLE

    def set_maintenance(self):
        """Sets the space status to under maintenance."""
        self._space_status = Space.STATUS_MAINTENANCE

    def get_space_status_display(self):
        """Returns a human-readable string for the current space status.

        Returns:
            A string describing the current status.
        """
        if self._space_status == Space.STATUS_AVAILABLE:
            return "Available"
        elif self._space_status == Space.STATUS_RESERVED:
            return "Reserved"
        elif self._space_status == Space.STATUS_MAINTENANCE:
            return "Under Maintenance"
        else:
            return "Unknown Status"

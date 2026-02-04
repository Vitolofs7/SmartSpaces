class Space:
    STATUS_AVAILABLE = "AVAILABLE"
    STATUS_RESERVED = "RESERVED"
    STATUS_MAINTENANCE = "MAINTENANCE"
    TYPE_GENERIC = "Basic Space"

    def __init__(self, space_id, space_name, capacity, space_type=None):
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
        return f"[{self.space_id}] {self.space_name}\n  • Type: {self.space_type}\n  • Status: {self.space_status}\n  • Capacity: {self.capacity}"

    @property
    def space_id(self):
        return self.__space_id

    @space_id.setter
    def space_id(self, value):
        self.__space_id = value

    @property
    def space_name(self):
        return self.__space_name

    @space_name.setter
    def space_name(self, value):
        self.__space_name = value

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        if value <= 0: raise ValueError("Capacity must be > 0")
        self.__capacity = value

    @property
    def space_status(self):
        return self._space_status

    @space_status.setter
    def space_status(self, value):
        if value not in (Space.STATUS_AVAILABLE, Space.STATUS_RESERVED, Space.STATUS_MAINTENANCE):
            raise ValueError("Invalid status")
        self._space_status = value

    @property
    def space_type(self):
        return self._space_type

    def is_available(self):
        return self._space_status == Space.STATUS_AVAILABLE

    def is_reserved(self):
        return self._space_status == Space.STATUS_RESERVED

    def reserve(self):
        if self._space_status != Space.STATUS_AVAILABLE: raise ValueError("Space not available")
        self._space_status = Space.STATUS_RESERVED

    def release(self):
        if self._space_status != Space.STATUS_RESERVED: raise ValueError("Space not reserved")
        self._space_status = Space.STATUS_AVAILABLE

    def set_maintenance(self):
        self._space_status = Space.STATUS_MAINTENANCE

    def get_space_status_display(self):
        return {"AVAILABLE": "Available", "RESERVED": "Reserved", "MAINTENANCE": "Under Maintenance"}.get(
            self._space_status, "Unknown")

# domain/space.py
class Space:
    STATUS_AVAILABLE = "AVAILABLE"
    STATUS_RESERVED = "RESERVED"
    STATUS_MAINTENANCE = "MAINTENANCE"

    def __init__(self, space_id, space_name, capacity):
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
        self._bookings = {}

    def __str__(self):
        return f"{self.space_name} ({self._space_status})"

    # getters
    @property
    def space_id(self):
        return self.__space_id

    @property
    def space_name(self):
        return self.__space_name

    @property
    def capacity(self):
        return self.__capacity

    @property
    def space_status(self):
        return self._space_status

    @space_id.setter
    def space_id(self, new_space_id):
        self.__space_id = new_space_id

    @space_name.setter
    def space_name(self, new_space_name):
        self.__space_name = new_space_name

    @capacity.setter
    def capacity(self, new_capacity):
        if new_capacity <= 0:
            raise ValueError("Capacity must be greater than zero.")
        self.__capacity = new_capacity

    @space_status.setter
    def space_status(self, new_space_status):
        if new_space_status not in (
                Space.STATUS_AVAILABLE,
                Space.STATUS_RESERVED,
                Space.STATUS_MAINTENANCE
        ):
            raise ValueError("Invalid space status.")
        self._space_status = new_space_status

    def is_available(self):
        return self._space_status == Space.STATUS_AVAILABLE

    def is_reserved(self):
        return self._space_status == Space.STATUS_RESERVED

    def reserve(self):
        if self._space_status == Space.STATUS_MAINTENANCE:
            raise ValueError("Cannot reserve a space under maintenance.")
        if self._space_status != Space.STATUS_AVAILABLE:
            raise ValueError("Space is not available for reservation.")
        self._space_status = Space.STATUS_RESERVED

    def release(self):
        if self._space_status == Space.STATUS_MAINTENANCE:
            raise ValueError("Cannot release a space under maintenance.")
        if self._space_status != Space.STATUS_RESERVED:
            raise ValueError("Space is not reserved.")
        self._space_status = Space.STATUS_AVAILABLE

    def set_maintenance(self):
        self._space_status = Space.STATUS_MAINTENANCE

    def get_space_status_display(self):
        if self._space_status == Space.STATUS_AVAILABLE:
            return "Available"
        elif self._space_status == Space.STATUS_RESERVED:
            return "Reserved"
        elif self._space_status == Space.STATUS_MAINTENANCE:
            return "Under Maintenance"
        else:
            return "Unknown Status"

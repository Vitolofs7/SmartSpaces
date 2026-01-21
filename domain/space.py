# domain/space.py
class Space:
    STATUS_AVAILABLE = "AVAILABLE"
    STATUS_RESERVED = "RESERVED"
    STATUS_MAINTENANCE = "MAINTENANCE"

    def __init__(self, space_id, space_name, capacity):
        space_id = (space_id or "").strip()
        space_name = (space_name or "").strip()

        if not space_id:
            raise ValueError("El identificador del espacio no puede estar vacío.")
        if not space_name:
            raise ValueError("El nombre del espacio no puede estar vacío.")
        if capacity <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        self.__space_id = space_id
        self.__space_name = space_name
        self.__capacity = capacity
        self._status = Space.STATUS_AVAILABLE
        self._bookings = {}

    def __str__(self):
        return f"{self.space_name} ({self._status})"

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
    def status(self):
        return self._status

    @space_id.setter
    def space_id(self, new_space_id):
        self.__space_id = new_space_id

    @space_name.setter
    def space_name(self, new_space_name):
        self.__space_name = new_space_name

    @capacity.setter
    def capacity(self, new_capacity):
        self.__capacity = new_capacity

    @status.setter
    def status(self, new_status):
        if new_status not in (
                Space.STATUS_AVAILABLE,
                Space.STATUS_RESERVED,
                Space.STATUS_MAINTENANCE
        ):
            raise ValueError("Estado de espacio no válido.")
        self._status = new_status

    def is_available(self):
        return self._status == Space.STATUS_AVAILABLE

    def is_reserved(self):
        return self._status == Space.STATUS_RESERVED

    def reserve(self):
        if self._status != Space.STATUS_AVAILABLE:
            raise ValueError("El espacio no está disponible para reservar.")
        self._status = Space.STATUS_RESERVED

    def release(self):
        if self._status != Space.STATUS_RESERVED:
            raise ValueError("El espacio no está reservado.")
        self._status = Space.STATUS_AVAILABLE

    def set_maintenance(self):
        self._status = Space.STATUS_MAINTENANCE

    def get_status_display(self):
        if self._status == Space.STATUS_AVAILABLE:
            return "Available"
        elif self._status == Space.STATUS_RESERVED:
            return "Reserved"
        elif self._status == Space.STATUS_MAINTENANCE:
            return "Under Maintenance"
        else:
            return "Unknown Status"

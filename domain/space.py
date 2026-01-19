# domain/space.py
class Space:

    def __init__(self, space_id, space_name, capacity):
        self.__space_id = space_id  # Identificador unico del espacio
        self.__space_name = space_name  # Nombre del espacio
        self.__capacity = capacity  # Capacidad maxima de personas
        self._status = "AVAILABLE"  # Estado del espacio (Available, Reserved, Maintenance)
        self.__bookings = {}  # Diccionario de reservas asociadas

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

    @property
    def bookings(self):
        return self.__bookings

    # setters
    @space_id.setter
    def space_id(self, new_space_id):
        self.__space_id = new_space_id

    @space_name.setter
    def space_name(self, new_space_name):
        self.__space_id = new_space_name

    @capacity.setter
    def capacity(self, new_capacity):
        self.__capacity = new_capacity

    @status.setter
    def status(self, new_status):
        self._status = new_status

    # metodos
    def is_reserved(self):
        if self._status == "RESERVED":
            return True
        return False


s = Space("1", "casa_echegey", 1)

print(s.status)
print(s.is_reserved())

from domain.space import Space


class SpaceMeetingroom(Space):
    TYPE = "Meeting room"

    def __init__(self, space_id, space_name, capacity, room_number, floor, equipment_list, num_power_outlets):
        super().__init__(space_id, space_name, capacity, space_type=SpaceMeetingroom.TYPE)
        self.__room_number, self.__floor, self.__num_power_outlets = room_number, floor, num_power_outlets
        self.__equipment_list = equipment_list or []
        self._validate_room_number(room_number)
        self._validate_floor(floor)
        self._validate_num_power_outlets(num_power_outlets)

    def __str__(self):
        eq = ', '.join(self.equipment_list) or 'None'
        return f"[{self.space_id}] {self.space_name}\n  • Type: {self.space_type}\n  • Status: {self.space_status}\n  • Capacity: {self.capacity}\n  • Room number: {self.room_number}\n  • Floor: {self.floor}\n  • Power outlets: {self.num_power_outlets}\n  • Equipment: {eq}"

    @property
    def room_number(self):
        return self.__room_number

    @room_number.setter
    def room_number(self, v):
        self._validate_room_number(v); self.__room_number = v

    @property
    def floor(self):
        return self.__floor

    @floor.setter
    def floor(self, v):
        self._validate_floor(v); self.__floor = v

    @property
    def num_power_outlets(self):
        return self.__num_power_outlets

    @num_power_outlets.setter
    def num_power_outlets(self, v):
        self._validate_num_power_outlets(v); self.__num_power_outlets = v

    @property
    def equipment_list(self):
        return list(self.__equipment_list)

    def _validate_room_number(self, v):
        if not isinstance(v, str) or not v.strip(): raise ValueError("Room number must be a non-empty string")

    def _validate_floor(self, v):
        if not isinstance(v, int) or v < 0: raise ValueError("Floor must be a non-negative integer")

    def _validate_num_power_outlets(self, v):
        if not isinstance(v, int) or v < 0: raise ValueError("Number of power outlets must be non-negative")

    def has_equipment(self, item):
        return item.lower() in (e.lower() for e in self.__equipment_list)

    def add_equipment(self, item):
        if not item or not isinstance(item, str): raise ValueError("Equipment must be non-empty string")
        if item not in self.__equipment_list: self.__equipment_list.append(item)

    def remove_equipment(self, item):
        if item in self.__equipment_list: self.__equipment_list.remove(item)

    def can_accommodate(self, n):
        if not isinstance(n, int) or n < 0: raise ValueError("Number must be non-negative")
        return n <= self.capacity

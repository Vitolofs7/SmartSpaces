from domain.space import Space


class SpaceMeetingroom(Space):
    TYPE = "Meeting room"

    def __init__(self, space_id, space_name, capacity, room_number, floor, equipment_list, num_power_outlets):
        super().__init__(space_id, space_name, capacity, space_type=SpaceMeetingroom.TYPE)
        self.__room_number = room_number
        self.__floor = floor
        self.__num_power_outlets = num_power_outlets
        self.__equipment_list = equipment_list or []

        self._space_type = "Meeting room"
        self._validate_room_number(room_number)
        self._validate_floor(floor)
        self._validate_num_power_outlets(num_power_outlets)

    def __str__(self):
        return (
            f"[{self.space_id}] {self.space_name}\n"
            f"  • Type: {self.space_type}\n"
            f"  • Status: {self.space_status}\n"
            f"  • Capacity: {self.capacity}\n"
            f"  • Room number: {self.room_number}\n"
            f"  • Floor: {self.floor}\n"
            f"  • Power outlets: {self.num_power_outlets}\n"
            f"  • Equipment: {', '.join(self.equipment_list) or 'None'}"
        )

    @property
    def room_number(self):
        return self.__room_number

    @room_number.setter
    def room_number(self, value):
        self._validate_room_number(value)
        self.__room_number = value

    @property
    def floor(self):
        return self.__floor

    @floor.setter
    def floor(self, value):
        self._validate_floor(value)
        self.__floor = value

    @property
    def num_power_outlets(self):
        return self.__num_power_outlets

    @num_power_outlets.setter
    def num_power_outlets(self, value):
        self._validate_num_power_outlets(value)
        self.__num_power_outlets = value

    @property
    def equipment_list(self):
        return list(self.__equipment_list)

    def _validate_room_number(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Room number must be a non-empty string.")

    def _validate_floor(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Floor must be a non-negative integer.")

    def _validate_num_power_outlets(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Number of power outlets must be a non-negative integer.")

    def has_equipment(self, item_name: str) -> bool:
        return item_name.lower() in (eq.lower() for eq in self.__equipment_list)

    def add_equipment(self, item_name: str):
        if not item_name or not isinstance(item_name, str):
            raise ValueError("Equipment name must be a non-empty string.")
        if item_name not in self.__equipment_list:
            self.__equipment_list.append(item_name)

    def remove_equipment(self, item_name: str):
        if item_name in self.__equipment_list:
            self.__equipment_list.remove(item_name)

    def can_accommodate(self, num_people: int) -> bool:
        if not isinstance(num_people, int) or num_people < 0:
            raise ValueError("Number of people must be a non-negative integer.")
        return num_people <= self.capacity

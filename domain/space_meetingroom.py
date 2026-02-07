# domain/space_meetingroom

from domain.space import Space


class SpaceMeetingroom(Space):
    """Domain entity representing a meeting room space.

    Extends the generic Space entity by adding meeting room specific
    attributes such as room number, floor, equipment, and available
    power outlets. It also provides validation and utility methods
    related to meeting room functionality.

    Attributes:
        TYPE: Constant indicating the type of space as a meeting room.
    """

    TYPE = "Meeting room"

    def __init__(self, space_id, space_name, capacity, room_number, floor, equipment_list, num_power_outlets):
        """Initializes a meeting room space.

        Args:
            space_id: Unique identifier of the meeting room.
            space_name: Name of the meeting room.
            capacity: Maximum occupancy of the meeting room.
            room_number: Room identifier or label.
            floor: Floor where the meeting room is located.
            equipment_list: List of available equipment.
            num_power_outlets: Number of available power outlets.

        Raises:
            ValueError: If room number, floor, or number of power outlets are invalid.
        """
        super().__init__(space_id, space_name, capacity, space_type=SpaceMeetingroom.TYPE)
        self.__room_number, self.__floor, self.__num_power_outlets = room_number, floor, num_power_outlets
        self.__equipment_list = equipment_list or []
        self._validate_room_number(room_number)
        self._validate_floor(floor)
        self._validate_num_power_outlets(num_power_outlets)

    def __str__(self):
        """Returns a human-readable representation of the meeting room.

        Returns:
            A formatted string describing the meeting room and its attributes.
        """
        eq = ', '.join(self.equipment_list) or 'None'
        return f"[{self.space_id}] {self.space_name}\n  • Type: {self.space_type}\n  • Status: {self.space_status}\n  • Capacity: {self.capacity}\n  • Room number: {self.room_number}\n  • Floor: {self.floor}\n  • Power outlets: {self.num_power_outlets}\n  • Equipment: {eq}"

    @property
    def room_number(self):
        """Returns the meeting room number.

        Returns:
            Room number string.
        """
        return self.__room_number

    @room_number.setter
    def room_number(self, v):
        """Sets the meeting room number.

        Args:
            v: New room number.

        Raises:
            ValueError: If the room number is invalid.
        """
        self._validate_room_number(v)
        self.__room_number = v

    @property
    def floor(self):
        """Returns the floor where the meeting room is located.

        Returns:
            Floor number.
        """
        return self.__floor

    @floor.setter
    def floor(self, v):
        """Sets the floor where the meeting room is located.

        Args:
            v: New floor number.

        Raises:
            ValueError: If the floor value is invalid.
        """
        self._validate_floor(v)
        self.__floor = v

    @property
    def num_power_outlets(self):
        """Returns the number of available power outlets.

        Returns:
            Number of power outlets.
        """
        return self.__num_power_outlets

    @num_power_outlets.setter
    def num_power_outlets(self, v):
        """Sets the number of available power outlets.

        Args:
            v: New number of power outlets.

        Raises:
            ValueError: If the number of power outlets is invalid.
        """
        self._validate_num_power_outlets(v)
        self.__num_power_outlets = v

    @property
    def equipment_list(self):
        """Returns a copy of the meeting room equipment list.

        Returns:
            List of equipment items.
        """
        return list(self.__equipment_list)

    def _validate_room_number(self, v):
        """Validates the meeting room number.

        Args:
            v: Room number value.

        Raises:
            ValueError: If the room number is not a valid non-empty string.
        """
        if not isinstance(v, str) or not v.strip(): raise ValueError("Room number must be a non-empty string")

    def _validate_floor(self, v):
        """Validates the floor number.

        Args:
            v: Floor value.

        Raises:
            ValueError: If the floor is not a non-negative integer.
        """
        if not isinstance(v, int) or v < 0: raise ValueError("Floor must be a non-negative integer")

    def _validate_num_power_outlets(self, v):
        """Validates the number of power outlets.

        Args:
            v: Number of power outlets.

        Raises:
            ValueError: If the number of power outlets is not a non-negative integer.
        """
        if not isinstance(v, int) or v < 0: raise ValueError("Number of power outlets must be non-negative")

    def has_equipment(self, item):
        """Checks whether the meeting room contains specific equipment.

        Args:
            item: Equipment name to search for.

        Returns:
            True if the equipment exists in the room, otherwise False.
        """
        return item.lower() in (e.lower() for e in self.__equipment_list)

    def add_equipment(self, item):
        """Adds equipment to the meeting room if not already present.

        Args:
            item: Equipment name to add.

        Raises:
            ValueError: If the equipment name is invalid.
        """
        if not item or not isinstance(item, str): raise ValueError("Equipment must be non-empty string")
        if item not in self.__equipment_list: self.__equipment_list.append(item)

    def remove_equipment(self, item):
        """Removes equipment from the meeting room if present.

        Args:
            item: Equipment name to remove.
        """
        if item in self.__equipment_list: self.__equipment_list.remove(item)

    def can_accommodate(self, n):
        """Checks if the meeting room can accommodate a given number of people.

        Args:
            n: Number of people.

        Returns:
            True if the meeting room capacity is sufficient, otherwise False.

        Raises:
            ValueError: If the number of people is invalid.
        """
        if not isinstance(n, int) or n < 0: raise ValueError("Number must be non-negative")
        return n <= self.capacity

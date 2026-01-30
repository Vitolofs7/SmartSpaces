from domain.space import Space


class SpaceMeetingroom(Space):
    """Represents a specialized meeting room space with additional attributes.

    Attributes:
        TYPE: Default type for meeting rooms.
    """

    TYPE = "Meeting room"

    def __init__(self, space_id, space_name, capacity, room_number, floor, equipment_list, num_power_outlets):
        """Initializes a SpaceMeetingroom instance.

        Args:
            space_id: Unique identifier for the space.
            space_name: Name of the meeting room.
            capacity: Maximum number of people the room can accommodate.
            room_number: Room number as a string.
            floor: Floor number as a non-negative integer.
            equipment_list: List of equipment names available in the room.
            num_power_outlets: Number of power outlets as a non-negative integer.

        Raises:
            ValueError: If any validation fails for room number, floor, or power outlets.
        """
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
        """Returns a string representation of the meeting room, including all attributes."""
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
        """Returns the room number."""
        return self.__room_number

    @room_number.setter
    def room_number(self, value):
        """Sets a new room number after validation.

        Raises:
            ValueError: If the room number is invalid.
        """
        self._validate_room_number(value)
        self.__room_number = value

    @property
    def floor(self):
        """Returns the floor number of the room."""
        return self.__floor

    @floor.setter
    def floor(self, value):
        """Sets a new floor number after validation.

        Raises:
            ValueError: If the floor number is invalid.
        """
        self._validate_floor(value)
        self.__floor = value

    @property
    def num_power_outlets(self):
        """Returns the number of power outlets in the room."""
        return self.__num_power_outlets

    @num_power_outlets.setter
    def num_power_outlets(self, value):
        """Sets a new number of power outlets after validation.

        Raises:
            ValueError: If the number is invalid.
        """
        self._validate_num_power_outlets(value)
        self.__num_power_outlets = value

    @property
    def equipment_list(self):
        """Returns a copy of the equipment list."""
        return list(self.__equipment_list)

    def _validate_room_number(self, value):
        """Validates the room number.

        Raises:
            ValueError: If the room number is not a non-empty string.
        """
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Room number must be a non-empty string.")

    def _validate_floor(self, value):
        """Validates the floor number.

        Raises:
            ValueError: If the floor is not a non-negative integer.
        """
        if not isinstance(value, int) or value < 0:
            raise ValueError("Floor must be a non-negative integer.")

    def _validate_num_power_outlets(self, value):
        """Validates the number of power outlets.

        Raises:
            ValueError: If the number is not a non-negative integer.
        """
        if not isinstance(value, int) or value < 0:
            raise ValueError("Number of power outlets must be a non-negative integer.")

    def has_equipment(self, item_name: str) -> bool:
        """Checks if the room has a specific piece of equipment.

        Args:
            item_name: Name of the equipment to check.

        Returns:
            True if the equipment is present, False otherwise.
        """
        return item_name.lower() in (eq.lower() for eq in self.__equipment_list)

    def add_equipment(self, item_name: str):
        """Adds a new piece of equipment to the room if not already present.

        Args:
            item_name: Name of the equipment to add.

        Raises:
            ValueError: If item_name is empty or not a string.
        """
        if not item_name or not isinstance(item_name, str):
            raise ValueError("Equipment name must be a non-empty string.")
        if item_name not in self.__equipment_list:
            self.__equipment_list.append(item_name)

    def remove_equipment(self, item_name: str):
        """Removes a piece of equipment from the room if present.

        Args:
            item_name: Name of the equipment to remove.
        """
        if item_name in self.__equipment_list:
            self.__equipment_list.remove(item_name)

    def can_accommodate(self, num_people: int) -> bool:
        """Checks if the room can accommodate a given number of people.

        Args:
            num_people: Number of people to check.

        Returns:
            True if the number of people is less than or equal to capacity.

        Raises:
            ValueError: If num_people is negative or not an integer.
        """
        if not isinstance(num_people, int) or num_people < 0:
            raise ValueError("Number of people must be a non-negative integer.")
        return num_people <= self.capacity

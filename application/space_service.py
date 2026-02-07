# application/space_service.py

from domain.space import Space
from domain.space_meetingroom import SpaceMeetingroom
from datetime import datetime


class SpaceService:
    """Application service responsible for managing spaces.

    This service handles the creation and retrieval of spaces, including
    specialized meeting rooms, and determines space availability based on
    active bookings.

    Args:
        space_repo: Repository responsible for storing and retrieving spaces.
    """

    def __init__(self, space_repo):
        """Initializes the space service with its repository.

        Args:
            space_repo: Repository used to manage space persistence.
        """
        self._space_repo = space_repo

    def create_space(self, space_id, space_name, capacity, space_type):
        """Creates a new generic space.

        Args:
            space_id: Unique identifier for the space.
            space_name: Name of the space.
            capacity: Maximum number of people allowed in the space.
            space_type: Type/category of the space.

        Returns:
            The newly created space instance.

        Raises:
            ValueError: If a space with the given ID already exists.
        """
        if self._space_repo.get(space_id): raise ValueError("Space with this ID already exists")
        s = Space(space_id, space_name, capacity, space_type)
        self._space_repo.save(s)
        return s

    def create_meeting_room(self, space_id, space_name, capacity, room_number, floor, num_power_outlets,
                            equipment_list):
        """Creates a new meeting room space with additional attributes.

        Args:
            space_id: Unique identifier for the meeting room.
            space_name: Name of the meeting room.
            capacity: Maximum number of people allowed in the meeting room.
            room_number: Room number identifier.
            floor: Floor where the meeting room is located.
            num_power_outlets: Number of available power outlets.
            equipment_list: List of equipment available in the meeting room.

        Returns:
            The newly created meeting room instance.

        Raises:
            ValueError: If a space with the given ID already exists.
        """
        if self._space_repo.get(space_id): raise ValueError("Space with this ID already exists")
        s = SpaceMeetingroom(space_id, space_name, capacity, room_number, floor, num_power_outlets=num_power_outlets,
                             equipment_list=equipment_list)
        self._space_repo.save(s)
        return s

    def list_spaces(self):
        """Retrieves all stored spaces.

        Returns:
            A list containing all spaces.
        """
        return self._space_repo.list()

    def get_available_spaces(self, booking_repo, start: datetime, end: datetime):
        """Retrieves spaces that do not have overlapping active bookings.

        Args:
            booking_repo: Repository used to retrieve bookings.
            start: Desired booking start datetime.
            end: Desired booking end datetime.

        Returns:
            A list of spaces available during the specified time range.
        """
        available_spaces = []
        for space in self._space_repo.list():
            bookings_for_space = [
                b for b in booking_repo.list()
                if b.space.space_id == space.space_id and b.is_active()
            ]

            if all(end <= b.start_time or start >= b.end_time for b in bookings_for_space):
                available_spaces.append(space)
        return available_spaces

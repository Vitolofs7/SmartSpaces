"""application/space_service.py"""

from domain.space import Space
from domain.space_meetingroom import SpaceMeetingRoom
from datetime import datetime


class SpaceService:
    """Application service responsible for managing spaces.

    This service handles the creation and retrieval of spaces, including
    specialized meeting rooms, and determines space availability based on
    active bookings. Space IDs are assigned automatically by the repository.

    Args:
        space_repo: Repository responsible for storing and retrieving spaces.
        booking_repo: Repository responsible for storing and retrieving bookings.
    """

    def __init__(self, space_repo, booking_repo):
        """Initializes the space service with its repositories.

        Args:
            space_repo: Repository used to manage space persistence.
            booking_repo: Repository used to retrieve bookings for availability checks.
        """
        self._space_repo = space_repo
        self._booking_repo = booking_repo

    def create_space(self, space_name, capacity, space_type):
        """Creates a new generic space.

        The space ID is assigned automatically by the repository.

        Args:
            space_name: Name of the space.
            capacity: Maximum number of people allowed in the space.
            space_type: Type/category of the space.

        Returns:
            The newly created space instance.
        """
        space = Space(None, space_name, capacity, space_type)
        self._space_repo.save(space)
        return space

    def create_meeting_room(self, space_name, capacity, room_number, floor, num_power_outlets, equipment_list):
        """Creates a new meeting room space with additional attributes.

        The space ID is assigned automatically by the repository.

        Args:
            space_name: Name of the meeting room.
            capacity: Maximum number of people allowed in the meeting room.
            room_number: Room number identifier.
            floor: Floor where the meeting room is located.
            num_power_outlets: Number of available power outlets.
            equipment_list: List of equipment available in the meeting room.

        Returns:
            The newly created meeting room instance.
        """
        space = SpaceMeetingRoom(None, space_name, capacity, room_number, floor,
                                 num_power_outlets=num_power_outlets,
                                 equipment_list=equipment_list)
        self._space_repo.save(space)
        return space

    def list_spaces(self):
        """Retrieves all stored spaces.

        Returns:
            A list containing all spaces.
        """
        return self._space_repo.list()

    def get_available_spaces(self, start: datetime, end: datetime):
        """Retrieves spaces that do not have overlapping active bookings.

        Args:
            start: Desired booking start datetime.
            end: Desired booking end datetime.

        Returns:
            A list of spaces available during the specified time range.
        """
        available_spaces = []
        for space in self._space_repo.list():
            bookings_for_space = [
                booking for booking in self._booking_repo.list()
                if booking.space.space_id == space.space_id and booking.is_active()
            ]
            if all(end <= booking.start_time or start >= booking.end_time for booking in bookings_for_space):
                available_spaces.append(space)
        return available_spaces

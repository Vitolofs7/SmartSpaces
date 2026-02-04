# application/space_service.py

from domain.space import Space
from domain.space_meetingroom import SpaceMeetingroom


class SpaceService:

    def __init__(self, space_repo):
        self._space_repo = space_repo

    def create_space(self, space_id, space_name, capacity, space_type):

        if self._space_repo.get(space_id):
            raise ValueError("Space with this ID already exists")

        space = Space(space_id, space_name, capacity, space_type)
        self._space_repo.save(space)

        return space

    def create_meeting_room(
            self,
            space_id,
            space_name,
            capacity,
            room_number,
            floor,
            num_power_outlets,
            equipment_list,
    ):

        if self._space_repo.get(space_id):
            raise ValueError("Space with this ID already exists")

        space = SpaceMeetingroom(
            space_id=space_id,
            space_name=space_name,
            capacity=capacity,
            room_number=room_number,
            floor=floor,
            num_power_outlets=num_power_outlets,
            equipment_list=equipment_list,
        )

        self._space_repo.save(space)

        return space

    def list_spaces(self):
        return self._space_repo.list()

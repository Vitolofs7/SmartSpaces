from domain.space import Space
from domain.space_meetingroom import SpaceMeetingroom


class SpaceService:
    def __init__(self, space_repo):
        self._space_repo = space_repo

    def create_space(self, space_id, space_name, capacity, space_type):
        if self._space_repo.get(space_id): raise ValueError("Space with this ID already exists")
        s = Space(space_id, space_name, capacity, space_type)
        self._space_repo.save(s)
        return s

    def create_meeting_room(self, space_id, space_name, capacity, room_number, floor, num_power_outlets,
                            equipment_list):
        if self._space_repo.get(space_id): raise ValueError("Space with this ID already exists")
        s = SpaceMeetingroom(space_id, space_name, capacity, room_number, floor, num_power_outlets=num_power_outlets,
                             equipment_list=equipment_list)
        self._space_repo.save(s)
        return s

    def list_spaces(self):
        return self._space_repo.list()

    def get_available_spaces(self, booking_repo, start_time, end_time):
        """Devuelve espacios que no tienen bookings activas que se solapen con el rango dado."""
        available = []
        for space in self._space_repo.list():
            bookings = [b for b in booking_repo.list() if b.space.space_id == space.space_id and b.is_active()]
            if all(not (start_time < b.end_time and b.start_time < end_time) for b in bookings):
                available.append(space)
        return available

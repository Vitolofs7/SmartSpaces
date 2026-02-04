from domain.space import Space
from domain.space_meetingroom import SpaceMeetingroom
from datetime import datetime


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

    def get_available_spaces(self, booking_repo, start: datetime, end: datetime):
        """Devuelve espacios disponibles que no tengan reservas activas solapadas con las fechas dadas."""
        available_spaces = []
        for space in self._space_repo.list():
            # obtener bookings activas para este espacio
            bookings_for_space = [
                b for b in booking_repo.list()
                if b.space.space_id == space.space_id and b.is_active()
            ]
            # comprobar si hay algún solapamiento
            if all(end <= b.start_time or start >= b.end_time for b in bookings_for_space):
                available_spaces.append(space)
        return available_spaces

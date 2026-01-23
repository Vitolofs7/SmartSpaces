from datetime import timedelta

class User:
    def __init__(self, user_id, name):
        user_id = (user_id or "").strip()
        name = (name or "").strip()

        if not user_id:
            raise ValueError("User id cannot be empty.")
        if not name:
            raise ValueError("User name cannot be empty.")

        self.__user_id = user_id
        self._name = name
        self._active = True

        # Default rules (basic behaviour)
        self._max_active_bookings = 1
        self._max_booking_duration = timedelta(hours=2)

    @property
    def user_id(self):
        return self.__user_id

    @property
    def name(self):
        return self._name

    def is_active(self):
        return self._active

    def deactivate(self):
        self._active = False

    def can_make_booking(self):
        return self._active

    @property
    def max_active_bookings(self):
        return self._max_active_bookings

    @property
    def max_booking_duration(self):
        return self._max_booking_duration

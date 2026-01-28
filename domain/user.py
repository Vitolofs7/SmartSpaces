from datetime import timedelta


class User:
    def __init__(self, user_id, name, surname1, surname2):
        user_id = (user_id or "").strip()
        name = (name or "").strip()
        surname1 = (surname1 or "").strip()
        surname2 = (surname2 or "").strip()

        if not user_id:
            raise ValueError("User id cannot be empty.")
        if not name:
            raise ValueError("User name cannot be empty.")
        if not surname1:
            raise ValueError("User first surname cannot be empty")
        if not surname2:
            raise ValueError("User second surname cannot be empty")

        self.__user_id = user_id
        self._name = name
        self._surname1 = surname1
        self._surname2 = surname2
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

    @property
    def surname1(self):
        return self._surname1

    @property
    def surname2(self):
        return self._surname2

    def full_name(self):
        return f"{self.name} {self.surname1} {self.surname2}"

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

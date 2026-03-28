"""tests/test_menu.py

Tests for all menu options in presentation/menu.py.
Uses unittest.mock to isolate the presentation layer from services.
"""

import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from io import StringIO


# ---------------------------------------------------------------------------
# Helpers: build fake domain objects
# ---------------------------------------------------------------------------

def make_space(space_id="S1", name="Conference Room", capacity=5,
               space_type="Basic", status="AVAILABLE"):
    space = MagicMock()
    space.space_id = space_id
    space.space_name = name
    space.capacity = capacity
    space.space_type = space_type
    space.space_status = status
    space.__str__ = lambda s: (
        f"[{s.space_id}] {s.space_name}\n"
        f"  • Type: {s.space_type}\n"
        f"  • Status: {s.space_status}\n"
        f"  • Capacity: {s.capacity}"
    )
    return space


def make_meeting_room(space_id="SM1", name="Main Meeting Room", capacity=8,
                      room_number="101", floor=1, outlets=4,
                      equipment=None, status="AVAILABLE"):
    room = make_space(space_id, name, capacity, "Meeting room", status)
    room.room_number = room_number
    room.floor = floor
    room.num_power_outlets = outlets
    room.equipment_list = equipment or ["Projector", "Whiteboard"]
    return room


def make_user(user_id="U1", full_name="Alice Smith Johnson", active=True):
    user = MagicMock()
    user.user_id = user_id
    user.full_name.return_value = full_name
    user.is_active.return_value = active
    return user


def make_booking(booking_id="B1", space=None, user=None,
                 start=None, end=None, status="ACTIVE"):
    now = datetime.now()
    booking = MagicMock()
    booking.booking_id = booking_id
    booking.space = space or make_space()
    booking.user = user or make_user()
    booking.start_time = start or now + timedelta(hours=1)
    booking.end_time = end or now + timedelta(hours=2)
    booking.status = status
    booking.is_active.return_value = (status == "ACTIVE")
    return booking


# ---------------------------------------------------------------------------
# Base test class: sets up service mocks and patches input/output
# ---------------------------------------------------------------------------

class MenuTestBase(unittest.TestCase):
    def setUp(self):
        self.space_service = MagicMock()
        self.user_service = MagicMock()
        self.booking_service = MagicMock()

        # Default return values
        self.space_service.list_spaces.return_value = [
            make_space("S1", "Conference Room"),
            make_meeting_room("SM1", "Main Meeting Room"),
        ]
        self.user_service.list_users.return_value = [
            make_user("U1", "Alice Smith Johnson"),
        ]
        self.booking_service.list_bookings.return_value = [
            make_booking(),
        ]

    def run_menu(self, inputs: list[str]) -> str:
        """Runs main() with patched services and captured I/O."""
        inputs_iter = iter(inputs)

        with patch("presentation.menu.SpaceSQLiteRepository"), \
             patch("presentation.menu.UserSQLiteRepository"), \
             patch("presentation.menu.BookingSQLiteRepository"), \
             patch("presentation.menu.seed_all"), \
             patch("presentation.menu.SpaceService", return_value=self.space_service), \
             patch("presentation.menu.UserService", return_value=self.user_service), \
             patch("presentation.menu.BookingService", return_value=self.booking_service), \
             patch("builtins.input", side_effect=inputs_iter), \
             patch("sys.stdout", new_callable=StringIO) as mock_out:
            from presentation.menu import main
            main()
            return mock_out.getvalue()


# ---------------------------------------------------------------------------
# Option 1 – List spaces
# ---------------------------------------------------------------------------

class TestOption1ListSpaces(MenuTestBase):
    def test_lists_all_spaces(self):
        output = self.run_menu(["1", "10"])
        self.space_service.list_spaces.assert_called()
        self.assertIn("Conference Room", output)
        self.assertIn("Main Meeting Room", output)


# ---------------------------------------------------------------------------
# Option 2 – List users
# ---------------------------------------------------------------------------

class TestOption2ListUsers(MenuTestBase):
    def test_lists_all_users(self):
        output = self.run_menu(["2", "10"])
        self.user_service.list_users.assert_called()
        self.assertIn("Alice Smith Johnson", output)


# ---------------------------------------------------------------------------
# Option 3 – List bookings
# ---------------------------------------------------------------------------

class TestOption3ListBookings(MenuTestBase):
    def test_lists_all_bookings(self):
        output = self.run_menu(["3", "10"])
        self.booking_service.list_bookings.assert_called()
        self.assertIn("B1", output)


# ---------------------------------------------------------------------------
# Option 4 – Create booking
# ---------------------------------------------------------------------------

class TestOption4CreateBooking(MenuTestBase):
    def test_create_booking_success(self):
        new_booking = make_booking("B2")
        self.booking_service.create_booking.return_value = new_booking

        future = datetime.now() + timedelta(days=2)
        start_str = future.strftime("%Y-%m-%d %H:%M")
        end_str = (future + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")

        output = self.run_menu([
            "4",
            "Alice Smith Johnson",  # select user
            "Conference Room",      # select space
            start_str,
            end_str,
            "10",
        ])
        self.booking_service.create_booking.assert_called_once()
        self.assertIn("B2", output)

    def test_create_booking_invalid_date_shows_error(self):
        output = self.run_menu([
            "4",
            "Alice Smith Johnson",
            "Conference Room",
            "not-a-date",           # bad date → ValueError
            "10",
        ])
        self.assertIn("Error", output)

    def test_create_booking_user_not_found(self):
        self.booking_service.create_booking.side_effect = ValueError("User not found")

        future = datetime.now() + timedelta(days=2)
        start_str = future.strftime("%Y-%m-%d %H:%M")
        end_str = (future + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M")

        output = self.run_menu([
            "4",
            "Unknown User",
            "Conference Room",
            start_str,
            end_str,
            "10",
        ])
        self.assertIn("Error", output)


# ---------------------------------------------------------------------------
# Option 5 – Cancel booking
# ---------------------------------------------------------------------------

class TestOption5CancelBooking(MenuTestBase):
    def test_cancel_booking_success(self):
        output = self.run_menu(["5", "B1", "10"])
        self.booking_service.cancel_booking.assert_called_once_with("B1")
        self.assertIn("cancelled", output.lower())

    def test_cancel_booking_not_found(self):
        self.booking_service.cancel_booking.side_effect = ValueError("Booking not found")
        output = self.run_menu(["5", "INVALID", "10"])
        self.assertIn("Error", output)

    def test_cancel_booking_not_active(self):
        self.booking_service.cancel_booking.side_effect = ValueError(
            "Only active bookings can be cancelled"
        )
        output = self.run_menu(["5", "B1", "10"])
        self.assertIn("Error", output)


# ---------------------------------------------------------------------------
# Option 6 – Finish booking
# ---------------------------------------------------------------------------

class TestOption6FinishBooking(MenuTestBase):
    def test_finish_booking_success(self):
        output = self.run_menu(["6", "B1", "10"])
        self.booking_service.finish_booking.assert_called_once_with("B1")
        self.assertIn("finished", output.lower())

    def test_finish_booking_not_found(self):
        self.booking_service.finish_booking.side_effect = ValueError("Booking not found")
        output = self.run_menu(["6", "INVALID", "10"])
        self.assertIn("Error", output)

    def test_finish_booking_not_active(self):
        self.booking_service.finish_booking.side_effect = ValueError(
            "Only active bookings can be finished"
        )
        output = self.run_menu(["6", "B1", "10"])
        self.assertIn("Error", output)


# ---------------------------------------------------------------------------
# Option 7 – Create space
# ---------------------------------------------------------------------------

class TestOption7CreateSpace(MenuTestBase):
    def test_create_generic_space(self):
        new_space = make_space("S3", "New Space")
        self.space_service.create_space.return_value = new_space

        output = self.run_menu(["7", "1", "New Space", "5", "10"])
        self.space_service.create_space.assert_called_once_with("New Space", 5, "Basic")
        self.assertIn("successfully", output.lower())

    def test_create_meeting_room(self):
        new_room = make_meeting_room("SM3", "New Room")
        self.space_service.create_meeting_room.return_value = new_room

        output = self.run_menu(["7", "2", "New Room", "6", "201", "2", "4", "TV,Projector", "10"])
        self.space_service.create_meeting_room.assert_called_once_with(
            "New Room", 6, "201", 2, 4, ["TV", "Projector"]
        )
        self.assertIn("successfully", output.lower())

    def test_create_meeting_room_no_equipment(self):
        new_room = make_meeting_room("SM4", "Empty Room", equipment=[])
        self.space_service.create_meeting_room.return_value = new_room

        output = self.run_menu(["7", "2", "Empty Room", "4", "202", "1", "2", "", "10"])
        args = self.space_service.create_meeting_room.call_args
        self.assertEqual(args[0][5], [])  # empty equipment list
        self.assertIn("successfully", output.lower())

    def test_create_space_invalid_type(self):
        output = self.run_menu(["7", "9", "Some Name", "5", "10"])
        self.space_service.create_space.assert_not_called()
        self.space_service.create_meeting_room.assert_not_called()


# ---------------------------------------------------------------------------
# Option 8 – List available spaces
# ---------------------------------------------------------------------------

class TestOption8ListAvailableSpaces(MenuTestBase):
    def test_available_spaces_found(self):
        self.space_service.get_available_spaces.return_value = [
            make_space("S2", "Open Space"),
        ]
        future = datetime.now() + timedelta(days=1)
        start_str = future.strftime("%Y-%m-%d %H:%M")
        end_str = (future + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")

        output = self.run_menu(["8", start_str, end_str, "10"])
        self.space_service.get_available_spaces.assert_called_once()
        self.assertIn("Open Space", output)

    def test_no_available_spaces(self):
        self.space_service.get_available_spaces.return_value = []
        future = datetime.now() + timedelta(days=1)
        start_str = future.strftime("%Y-%m-%d %H:%M")
        end_str = (future + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")

        output = self.run_menu(["8", start_str, end_str, "10"])
        self.assertIn("No spaces available", output)

    def test_available_spaces_invalid_date(self):
        output = self.run_menu(["8", "bad-date", "10"])
        self.assertIn("Error", output)


# ---------------------------------------------------------------------------
# Option 9 – Modify booking
# ---------------------------------------------------------------------------

class TestOption9ModifyBooking(MenuTestBase):
    def test_modify_booking_success(self):
        future = datetime.now() + timedelta(days=3)
        updated = make_booking("B1", start=future, end=future + timedelta(hours=2))
        self.booking_service.modify_booking.return_value = updated

        start_str = future.strftime("%Y-%m-%d %H:%M")
        end_str = (future + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")

        output = self.run_menu(["9", "B1", start_str, end_str, "10"])
        self.booking_service.modify_booking.assert_called_once()
        self.assertIn("B1", output)

    def test_modify_booking_not_found(self):
        self.booking_service.modify_booking.side_effect = ValueError("Booking not found")
        future = datetime.now() + timedelta(days=3)
        start_str = future.strftime("%Y-%m-%d %H:%M")
        end_str = (future + timedelta(hours=2)).strftime("%Y-%m-%d %H:%M")

        output = self.run_menu(["9", "INVALID", start_str, end_str, "10"])
        self.assertIn("Error", output)

    def test_modify_booking_invalid_date(self):
        output = self.run_menu(["9", "B1", "wrong-date", "10"])
        self.assertIn("Error", output)


# ---------------------------------------------------------------------------
# Option 10 – Exit
# ---------------------------------------------------------------------------

class TestOption10Exit(MenuTestBase):
    def test_exit_prints_goodbye(self):
        output = self.run_menu(["10"])
        self.assertIn("Goodbye", output)


# ---------------------------------------------------------------------------
# Invalid option
# ---------------------------------------------------------------------------

class TestInvalidOption(MenuTestBase):
    def test_invalid_option_shows_message(self):
        output = self.run_menu(["99", "10"])
        self.assertIn("Invalid option", output)


if __name__ == "__main__":
    unittest.main(verbosity=2)
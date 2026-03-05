import unittest
from datetime import timedelta
from domain.user import User


class TestUser(unittest.TestCase):

    def test_user_creation_success(self):
        user = User("U1", "John", "Doe", "Smith")
        self.assertEqual(user.user_id, "U1")
        self.assertEqual(user.name, "John")
        self.assertEqual(user.surname1, "Doe")
        self.assertEqual(user.surname2, "Smith")
        self.assertTrue(user.is_active())
        self.assertEqual(user.max_active_bookings, 1)
        self.assertEqual(user.max_booking_duration, timedelta(hours=2))
        self.assertEqual(user.full_name(), "John Doe Smith")

    def test_user_creation_invalid_fields(self):
        with self.assertRaises(ValueError):
            User("", "John", "Doe", "Smith")
        with self.assertRaises(ValueError):
            User("U1", "", "Doe", "Smith")
        with self.assertRaises(ValueError):
            User("U1", "John", "", "Smith")
        with self.assertRaises(ValueError):
            User("U1", "John", "Doe", "")

    def test_user_deactivation(self):
        user = User("U2", "Alice", "Brown", "Johnson")
        self.assertTrue(user.is_active())
        self.assertTrue(user.can_make_booking())

        user.deactivate()
        self.assertFalse(user.is_active())
        self.assertFalse(user.can_make_booking())

    def test_full_name_property(self):
        user = User("U3", "Bob", "White", "Black")
        self.assertEqual(user.full_name(), "Bob White Black")

    def test_max_booking_properties(self):
        user = User("U4", "Eve", "Green", "Blue")
        self.assertEqual(user.max_active_bookings, 1)
        self.assertEqual(user.max_booking_duration, timedelta(hours=2))


if __name__ == "__main__":
    unittest.main()

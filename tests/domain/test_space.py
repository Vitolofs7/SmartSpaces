import unittest
from domain.space import Space


class TestSpace(unittest.TestCase):

    def setUp(self):
        self.space = Space(space_id="S1", space_name="Conference Room", capacity=10)

    def test_space_creation_success(self):
        self.assertEqual(self.space.space_id, "S1")
        self.assertEqual(self.space.space_name, "Conference Room")
        self.assertEqual(self.space.capacity, 10)
        self.assertEqual(self.space.space_status, Space.STATUS_AVAILABLE)
        self.assertEqual(self.space.space_type, Space.TYPE_GENERIC)

    def test_space_creation_invalid_id(self):
        with self.assertRaises(ValueError):
            Space(space_id="", space_name="Room", capacity=5)

    def test_space_creation_invalid_name(self):
        with self.assertRaises(ValueError):
            Space(space_id="S2", space_name="", capacity=5)

    def test_space_creation_invalid_capacity(self):
        with self.assertRaises(ValueError):
            Space(space_id="S3", space_name="Room", capacity=0)

    def test_setters_and_getters(self):
        self.space.space_name = "New Name"
        self.assertEqual(self.space.space_name, "New Name")

        self.space.space_id = "S100"
        self.assertEqual(self.space.space_id, "S100")

        self.space.capacity = 20
        self.assertEqual(self.space.capacity, 20)

        with self.assertRaises(ValueError):
            self.space.capacity = 0

    def test_is_available_and_is_reserved(self):
        self.assertTrue(self.space.is_available())
        self.assertFalse(self.space.is_reserved())

        self.space.reserve()
        self.assertFalse(self.space.is_available())
        self.assertTrue(self.space.is_reserved())

        self.space.release()
        self.assertTrue(self.space.is_available())
        self.assertFalse(self.space.is_reserved())

        self.space.set_maintenance()
        self.assertFalse(self.space.is_available())
        self.assertFalse(self.space.is_reserved())
        self.assertEqual(self.space.space_status, Space.STATUS_MAINTENANCE)

    def test_reserve_error_when_not_available(self):
        self.space.set_maintenance()
        with self.assertRaises(ValueError):
            self.space.reserve()

    def test_release_error_when_not_reserved(self):
        with self.assertRaises(ValueError):
            self.space.release()

    def test_status_display(self):
        self.assertEqual(self.space.get_space_status_display(), "Available")
        self.space.reserve()
        self.assertEqual(self.space.get_space_status_display(), "Reserved")
        self.space.set_maintenance()
        self.assertEqual(self.space.get_space_status_display(), "Under Maintenance")

    def test_invalid_status_setter(self):
        with self.assertRaises(ValueError):
            self.space.space_status = "INVALID"


if __name__ == "__main__":
    unittest.main()

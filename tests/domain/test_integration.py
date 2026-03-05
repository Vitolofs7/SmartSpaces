"""tests/domain/test_integration.py"""

import unittest
from datetime import datetime, timedelta
from domain.booking import Booking
from domain.space import Space
from domain.user import User


class TestIntegrationBookingSystem(unittest.TestCase):

    def setUp(self):
        self.user1 = User("U1", "Alice", "Smith", "Johnson")
        self.user2 = User("U2", "Bob", "Brown", "Lee")
        self.user3 = User("U3", "Charlie", "King", "Wright")

        self.space1 = Space("S1", "Room A", 5)
        self.space2 = Space("S2", "Room B", 10)
        self.space3 = Space("S3", "Room C", 5)

        class FakeBookingRepo:
            def __init__(self):
                self.bookings = []

            def list(self):
                return self.bookings

            def save(self, booking):
                booking._booking_id = len(self.bookings) + 1
                self.bookings.append(booking)

        self.repo = FakeBookingRepo()

        self.start = datetime.now()
        self.end = self.start + timedelta(hours=2)
        self.later_start = self.end + timedelta(hours=1)
        self.later_end = self.later_start + timedelta(hours=2)

    def test_full_booking_flow(self):
        b1 = Booking.create(self.space1, self.user1, self.start, self.end, self.repo)
        self.assertTrue(b1.is_active())
        self.assertEqual(self.space1.space_status, Space.STATUS_RESERVED)

        b2 = Booking.create(self.space2, self.user2, self.start, self.end, self.repo)
        self.assertTrue(b2.is_active())
        self.assertEqual(self.space2.space_status, Space.STATUS_RESERVED)

        with self.assertRaises(ValueError):
            Booking.create(
                self.space1,
                self.user2,
                self.start + timedelta(minutes=30),
                self.end + timedelta(hours=1),
                self.repo
            )

        b1.cancel()
        self.assertEqual(b1.status, Booking.STATUS_CANCELLED)
        self.assertEqual(self.space1.space_status, Space.STATUS_AVAILABLE)

        b3 = Booking.create(
            self.space1,
            self.user2,
            self.start + timedelta(minutes=30),
            self.end + timedelta(minutes=30),
            self.repo
        )
        self.assertEqual(b3.space, self.space1)
        self.assertEqual(self.space1.space_status, Space.STATUS_RESERVED)

        b2.reschedule(self.later_start, self.later_end, self.repo)
        self.assertEqual(b2.start_time, self.later_start)
        self.assertEqual(b2.end_time, self.later_end)

        # Usar space3 para mantenimiento
        self.space3.set_maintenance()
        self.assertFalse(self.space3.is_available())
        self.assertFalse(self.space3.is_reserved())

        user4 = User("U4", "Diana", "White", "Miller")

        with self.assertRaises(ValueError):
            Booking.create(self.space3, self.user3, self.later_start, self.later_end, self.repo)

        b3.finish()
        self.assertEqual(b3.status, Booking.STATUS_FINISHED)
        self.assertEqual(self.space1.space_status, Space.STATUS_AVAILABLE)

        self.space1.set_maintenance()
        self.assertFalse(self.space1.is_available())
        self.assertFalse(self.space1.is_reserved())

        self.user1.deactivate()
        with self.assertRaises(ValueError):
            Booking.create(self.space1, self.user1, self.later_start, self.later_end, self.repo)

        booking_ids = {b.booking_id for b in self.repo.list()}
        self.assertEqual(len(booking_ids), len(self.repo.list()))
        self.assertTrue(all(id_ is not None for id_ in booking_ids))


if __name__ == "__main__":
    unittest.main()

"""tests/domain/test_booking.py

Tests for the Booking domain entity.
Covers creation, cancellation, finishing, overlap detection, and rescheduling.
"""

import unittest
from datetime import datetime, timedelta
from domain.booking import Booking
from domain.space import Space
from domain.user import User


class FakeBookingRepo:
    """Minimal fake repository for testing Booking domain logic."""

    def __init__(self):
        self.bookings = []
        self._last_id = 0

    def list(self):
        return list(self.bookings)

    def save(self, booking):
        self._last_id += 1
        booking._booking_id = f"B{self._last_id}"
        self.bookings.append(booking)


class TestBookingCreation(unittest.TestCase):

    def setUp(self):
        self.user = User("U1", "Alice", "Smith", "Johnson")
        self.space = Space("S1", "Room A", 5)
        self.repo = FakeBookingRepo()
        self.start = datetime.now() + timedelta(hours=1)
        self.end = self.start + timedelta(hours=1)

    def test_booking_creation_success(self):
        booking = Booking(self.space, self.user, self.start, self.end)
        self.assertEqual(booking.space, self.space)
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.start_time, self.start)
        self.assertEqual(booking.end_time, self.end)
        self.assertTrue(booking.is_active())
        self.assertIsNone(booking.booking_id)

    def test_booking_creation_invalid_times(self):
        with self.assertRaises(ValueError):
            Booking(self.space, self.user, self.end, self.start)

    def test_booking_creation_same_times(self):
        with self.assertRaises(ValueError):
            Booking(self.space, self.user, self.start, self.start)

    def test_create_via_factory(self):
        booking = Booking.create(self.space, self.user, self.start, self.end, self.repo)
        self.assertTrue(booking.is_active())
        self.assertEqual(booking.space, self.space)
        self.assertEqual(self.space.space_status, Space.STATUS_RESERVED)

    def test_create_inactive_user_raises(self):
        self.user.deactivate()
        with self.assertRaises(ValueError):
            Booking.create(self.space, self.user, self.start, self.end, self.repo)

    def test_create_maintenance_space_raises(self):
        self.space.set_maintenance()
        with self.assertRaises(ValueError):
            Booking.create(self.space, self.user, self.start, self.end, self.repo)


class TestBookingOverlap(unittest.TestCase):

    def setUp(self):
        self.user1 = User("U1", "Alice", "Smith", "Johnson")
        self.user2 = User("U2", "Bob", "Brown", "Taylor")
        self.space = Space("S1", "Room A", 5)
        self.repo = FakeBookingRepo()
        self.start = datetime.now() + timedelta(hours=1)
        self.end = self.start + timedelta(hours=2)

    def test_overlapping_bookings_raises(self):
        b1 = Booking.create(self.space, self.user1, self.start, self.end, self.repo)
        self.repo.save(b1)
        with self.assertRaises(ValueError):
            Booking.create(
                self.space, self.user2,
                self.start + timedelta(minutes=30),
                self.end + timedelta(minutes=30),
                self.repo
            )

    def test_non_overlapping_bookings_succeed(self):
        b1 = Booking.create(self.space, self.user1, self.start, self.end, self.repo)
        self.repo.save(b1)
        later_start = self.end + timedelta(hours=1)
        later_end = later_start + timedelta(hours=1)
        b2 = Booking.create(self.space, self.user2, later_start, later_end, self.repo)
        self.assertIsNotNone(b2)

    def test_overlaps_with_method(self):
        b1 = Booking(self.space, self.user1, self.start, self.end)
        b2 = Booking(self.space, self.user2,
                     self.start + timedelta(minutes=30),
                     self.end + timedelta(minutes=30))
        self.assertTrue(b1.overlaps_with(b2))

    def test_no_overlap_adjacent(self):
        b1 = Booking(self.space, self.user1, self.start, self.end)
        b2 = Booking(self.space, self.user2, self.end, self.end + timedelta(hours=1))
        self.assertFalse(b1.overlaps_with(b2))

    def test_cancelled_booking_no_overlap(self):
        b1 = Booking(self.space, self.user1, self.start, self.end)
        b1._booking_status = Booking.STATUS_CANCELLED
        b2 = Booking(self.space, self.user2, self.start, self.end)
        self.assertFalse(b1.overlaps_with(b2))


class TestBookingCancel(unittest.TestCase):

    def setUp(self):
        self.user = User("U1", "Alice", "Smith", "Johnson")
        self.space = Space("S1", "Room A", 5)
        self.start = datetime.now() + timedelta(hours=1)
        self.end = self.start + timedelta(hours=1)

    def test_cancel_active_booking(self):
        self.space.reserve()
        booking = Booking(self.space, self.user, self.start, self.end)
        booking.cancel()
        self.assertEqual(booking.status, Booking.STATUS_CANCELLED)
        self.assertEqual(self.space.space_status, Space.STATUS_AVAILABLE)

    def test_cancel_non_active_raises(self):
        self.space.reserve()
        booking = Booking(self.space, self.user, self.start, self.end)
        booking.cancel()
        with self.assertRaises(ValueError):
            booking.cancel()


class TestBookingFinish(unittest.TestCase):

    def setUp(self):
        self.user = User("U1", "Alice", "Smith", "Johnson")
        self.space = Space("S1", "Room A", 5)
        self.start = datetime.now() + timedelta(hours=1)
        self.end = self.start + timedelta(hours=1)

    def test_finish_active_booking(self):
        self.space.reserve()
        booking = Booking(self.space, self.user, self.start, self.end)
        booking.finish()
        self.assertEqual(booking.status, Booking.STATUS_FINISHED)
        self.assertEqual(self.space.space_status, Space.STATUS_AVAILABLE)

    def test_finish_non_active_raises(self):
        self.space.reserve()
        booking = Booking(self.space, self.user, self.start, self.end)
        booking.finish()
        with self.assertRaises(ValueError):
            booking.finish()


class TestBookingReschedule(unittest.TestCase):

    def setUp(self):
        self.user1 = User("U1", "Alice", "Smith", "Johnson")
        self.user2 = User("U2", "Bob", "Brown", "Taylor")
        self.space = Space("S1", "Room A", 5)
        self.repo = FakeBookingRepo()
        self.start = datetime.now() + timedelta(hours=1)
        self.end = self.start + timedelta(hours=2)

    def test_reschedule_success(self):
        booking = Booking(self.space, self.user1, self.start, self.end)
        booking._booking_id = "B1"
        new_start = self.end + timedelta(hours=1)
        new_end = new_start + timedelta(hours=1)
        booking.reschedule(new_start, new_end, self.repo)
        self.assertEqual(booking.start_time, new_start)
        self.assertEqual(booking.end_time, new_end)

    def test_reschedule_invalid_times_raises(self):
        booking = Booking(self.space, self.user1, self.start, self.end)
        booking._booking_id = "B1"
        with self.assertRaises(ValueError):
            booking.reschedule(self.end, self.start, self.repo)

    def test_reschedule_non_active_raises(self):
        self.space.reserve()
        booking = Booking(self.space, self.user1, self.start, self.end)
        booking._booking_id = "B1"
        booking.cancel()
        new_start = self.end + timedelta(hours=1)
        new_end = new_start + timedelta(hours=1)
        with self.assertRaises(ValueError):
            booking.reschedule(new_start, new_end, self.repo)

    def test_reschedule_overlap_raises(self):
        b1 = Booking.create(self.space, self.user1, self.start, self.end, self.repo)
        self.repo.save(b1)

        later_start = self.end + timedelta(hours=1)
        later_end = later_start + timedelta(hours=2)
        b2 = Booking.create(self.space, self.user2, later_start, later_end, self.repo)
        self.repo.save(b2)

        with self.assertRaises(ValueError):
            b2.reschedule(
                self.start + timedelta(minutes=30),
                self.end + timedelta(minutes=30),
                self.repo
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
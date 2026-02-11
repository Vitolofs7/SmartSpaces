import unittest
from datetime import datetime, timedelta
from domain.booking import Booking


class FakeUser:
    def __init__(self, active=True):
        self._active = active

    def is_active(self):
        return self._active


class FakeSpace:
    def __init__(self, space_id=1, name="Room A", available=True):
        self.space_id = space_id
        self.space_name = name
        self._available = available
        self.reserved = False
        self.released = False

    def is_available(self):
        return self._available

    def reserve(self):
        self.reserved = True
        self._available = False

    def release(self):
        self.released = True
        self._available = True


class FakeBookingRepo:
    def __init__(self):
        self.bookings = []

    def list(self):
        return self.bookings

    def save(self, booking):
        self.bookings.append(booking)


class TestBooking(unittest.TestCase):

    def setUp(self):
        self.user = FakeUser(True)
        self.space = FakeSpace()
        self.repo = FakeBookingRepo()

        self.start = datetime.now()
        self.end = self.start + timedelta(hours=2)

    def test_create_booking_success(self):
        booking = Booking.create(
            self.space, self.user, self.start, self.end, self.repo
        )

        self.assertTrue(booking.is_active())
        self.assertTrue(self.space.reserved)
        self.assertEqual(len(self.repo.bookings), 1)

    def test_create_booking_inactive_user(self):
        inactive_user = FakeUser(False)

        with self.assertRaises(ValueError):
            Booking.create(self.space, inactive_user, self.start, self.end, self.repo)

    def test_create_booking_space_not_available(self):
        space = FakeSpace(available=False)

        with self.assertRaises(ValueError):
            Booking.create(space, self.user, self.start, self.end, self.repo)

    def test_create_booking_overlapping(self):
        Booking.create(self.space, self.user, self.start, self.end, self.repo)

        with self.assertRaises(ValueError):
            Booking.create(
                self.space,
                self.user,
                self.start + timedelta(minutes=30),
                self.end + timedelta(hours=1),
                self.repo
            )

    def test_cancel_booking(self):
        booking = Booking.create(self.space, self.user, self.start, self.end, self.repo)

        booking.cancel()

        self.assertEqual(booking.status, Booking.STATUS_CANCELLED)
        self.assertTrue(self.space.released)

    def test_cancel_non_active_booking(self):
        booking = Booking.create(self.space, self.user, self.start, self.end, self.repo)
        booking.cancel()

        with self.assertRaises(ValueError):
            booking.cancel()

    def test_finish_booking(self):
        booking = Booking.create(self.space, self.user, self.start, self.end, self.repo)

        booking.finish()

        self.assertEqual(booking.status, Booking.STATUS_FINISHED)
        self.assertTrue(self.space.released)

    def test_overlap_true(self):
        b1 = Booking(self.space, self.user, self.start, self.end)
        b2 = Booking(
            self.space,
            self.user,
            self.start + timedelta(minutes=30),
            self.end + timedelta(hours=1)
        )

        self.assertTrue(b1.overlaps_with(b2))

    def test_overlap_false(self):
        b1 = Booking(self.space, self.user, self.start, self.end)
        b2 = Booking(
            self.space,
            self.user,
            self.end + timedelta(minutes=1),
            self.end + timedelta(hours=2)
        )

        self.assertFalse(b1.overlaps_with(b2))

    def test_reschedule_success(self):
        booking = Booking.create(self.space, self.user, self.start, self.end, self.repo)

        new_start = self.end + timedelta(hours=1)
        new_end = new_start + timedelta(hours=2)

        booking.reschedule(new_start, new_end, self.repo)

        self.assertEqual(booking.start_time, new_start)
        self.assertEqual(booking.end_time, new_end)

    def test_reschedule_overlap(self):
        b1 = Booking.create(self.space, self.user, self.start, self.end, self.repo)

        b2 = Booking.create(
            FakeSpace(space_id=self.space.space_id),
            self.user,
            self.end + timedelta(hours=1),
            self.end + timedelta(hours=3),
            self.repo
        )

        with self.assertRaises(ValueError):
            b2.reschedule(self.start, self.end, self.repo)

    def test_reschedule_non_active_booking(self):
        booking = Booking.create(self.space, self.user, self.start, self.end, self.repo)
        booking.cancel()

        with self.assertRaises(ValueError):
            booking.reschedule(self.start, self.end, self.repo)


if __name__ == "__main__":
    unittest.main()

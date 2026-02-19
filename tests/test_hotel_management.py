"""Unit tests for hotel_management.py."""

import unittest
import os
import json
from hotel_management import (
    Customer, Hotel, Reservation, JSON_FILE, _load
)


def _reset() -> None:
    """Remove the data file to start each test with a clean state."""
    if os.path.exists(JSON_FILE):
        os.remove(JSON_FILE)


class TestLoad(unittest.TestCase):
    """Tests for the _load helper."""

    def setUp(self) -> None:
        """Reset data file before each test."""
        _reset()

    def test_load_no_file(self) -> None:
        """Returns default structure when data file does not exist."""
        data = _load()
        self.assertEqual(data, {
            "hotels": {}, "customers": {}, "reservations": {}
        })

    def test_load_existing_file(self) -> None:
        """Returns correct data when data file exists."""
        payload = {"hotels": {}, "customers": {"C1": {}}, "reservations": {}}
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f)
        data = _load()
        self.assertIn("C1", data["customers"])


class TestCustomer(unittest.TestCase):
    """Tests for the Customer class."""

    def setUp(self) -> None:
        """Reset data file and create a base customer before each test."""
        _reset()
        Customer("C1", "Alice", "alice@example.com").create()

    def test_create(self) -> None:
        """Customer is persisted after create()."""
        data = _load()
        self.assertIn("C1", data["customers"])
        self.assertEqual(data["customers"]["C1"]["name"], "Alice")

    def test_create_duplicate_raises(self) -> None:
        """Creating a customer with a duplicate ID raises ValueError."""
        with self.assertRaises(ValueError):
            Customer("C1", "Alice", "alice@example.com").create()

    def test_delete(self) -> None:
        """Customer is removed from storage after delete()."""
        Customer.delete("C1")
        data = _load()
        self.assertNotIn("C1", data["customers"])

    def test_delete_not_found_raises(self) -> None:
        """Deleting a non-existent customer raises ValueError."""
        with self.assertRaises(ValueError):
            Customer.delete("UNKNOWN")

    def test_display(self) -> None:
        """display() runs without errors for an existing customer."""
        Customer.display_customer_info("C1")

    def test_display_not_found_raises(self) -> None:
        """Displaying a non-existent customer raises ValueError."""
        with self.assertRaises(ValueError):
            Customer.display_customer_info("UNKNOWN")

    def test_modify_name(self) -> None:
        """modify() updates the customer name correctly."""
        Customer.modify("C1", name="Bob")
        data = _load()
        self.assertEqual(data["customers"]["C1"]["name"], "Bob")

    def test_modify_email(self) -> None:
        """modify() updates the customer email correctly."""
        Customer.modify("C1", email="new@example.com")
        data = _load()
        self.assertEqual(data["customers"]["C1"]["email"], "new@example.com")

    def test_modify_not_found_raises(self) -> None:
        """Modifying a non-existent customer raises ValueError."""
        with self.assertRaises(ValueError):
            Customer.modify("UNKNOWN", name="Bob")


class TestHotel(unittest.TestCase):
    """Tests for the Hotel class."""

    def setUp(self) -> None:
        """Reset data file and create a base hotel before each test."""
        _reset()
        Hotel("H1", "Grand Palace", 10).create()

    def test_create(self) -> None:
        """Hotel is persisted after create()."""
        data = _load()
        self.assertIn("H1", data["hotels"])
        self.assertEqual(data["hotels"]["H1"]["name"], "Grand Palace")

    def test_create_duplicate_raises(self) -> None:
        """Creating a hotel with a duplicate ID raises ValueError."""
        with self.assertRaises(ValueError):
            Hotel("H1", "Grand Palace", 10).create()

    def test_delete(self) -> None:
        """Hotel is removed from storage after delete()."""
        Hotel.delete("H1")
        data = _load()
        self.assertNotIn("H1", data["hotels"])

    def test_delete_not_found_raises(self) -> None:
        """Deleting a non-existent hotel raises ValueError."""
        with self.assertRaises(ValueError):
            Hotel.delete("UNKNOWN")

    def test_display(self) -> None:
        """display() runs without errors for an existing hotel."""
        Hotel.display_hotel_info("H1")

    def test_display_not_found_raises(self) -> None:
        """Displaying a non-existent hotel raises ValueError."""
        with self.assertRaises(ValueError):
            Hotel.display_hotel_info("UNKNOWN")

    def test_modify_name(self) -> None:
        """modify() updates the hotel name correctly."""
        Hotel.modify("H1", name="New Name")
        data = _load()
        self.assertEqual(data["hotels"]["H1"]["name"], "New Name")

    def test_modify_total_rooms(self) -> None:
        """modify() updates the total rooms correctly."""
        Hotel.modify("H1", total_rooms=20)
        data = _load()
        self.assertEqual(data["hotels"]["H1"]["total_rooms"], 20)

    def test_modify_not_found_raises(self) -> None:
        """Modifying a non-existent hotel raises ValueError."""
        with self.assertRaises(ValueError):
            Hotel.modify("UNKNOWN", name="X")

    def test_reserve_room(self) -> None:
        """reserve_room() marks the room as reserved."""
        Hotel.reserve_room("H1", 1)
        data = _load()
        self.assertIn(1, data["hotels"]["H1"]["reserved_rooms"])

    def test_reserve_room_hotel_not_found_raises(self) -> None:
        """Reserving a room in a non-existent hotel raises ValueError."""
        with self.assertRaises(ValueError):
            Hotel.reserve_room("UNKNOWN", 1)

    def test_reserve_room_out_of_range_raises(self) -> None:
        """Reserving a room number beyond total_rooms raises ValueError."""
        with self.assertRaises(ValueError):
            Hotel.reserve_room("H1", 99)

    def test_reserve_room_already_reserved_raises(self) -> None:
        """Reserving an already reserved room raises ValueError."""
        Hotel.reserve_room("H1", 1)
        with self.assertRaises(ValueError):
            Hotel.reserve_room("H1", 1)

    def test_cancel_room(self) -> None:
        """cancel_room() removes the room from reserved list."""
        Hotel.reserve_room("H1", 1)
        Hotel.cancel_room("H1", 1)
        data = _load()
        self.assertNotIn(1, data["hotels"]["H1"]["reserved_rooms"])

    def test_cancel_room_hotel_not_found_raises(self) -> None:
        """Cancelling a room in a non-existent hotel raises ValueError."""
        with self.assertRaises(ValueError):
            Hotel.cancel_room("UNKNOWN", 1)

    def test_cancel_room_not_reserved_raises(self) -> None:
        """Cancelling a room that is not reserved raises ValueError."""
        with self.assertRaises(ValueError):
            Hotel.cancel_room("H1", 1)


class TestReservation(unittest.TestCase):
    """Tests for the Reservation class."""

    def setUp(self) -> None:
        """Reset data file and create base customer and hotel."""
        _reset()
        Customer("C1", "Alice", "alice@example.com").create()
        Hotel("H1", "Grand Palace", 10).create()

    def test_create(self) -> None:
        """Reservation is persisted and rooms are marked reserved."""
        Reservation("R1", "C1", "H1", [1, 2], "2026-03-01",
                    "2026-03-05").create()
        data = _load()
        self.assertIn("R1", data["reservations"])
        self.assertIn(1, data["hotels"]["H1"]["reserved_rooms"])
        self.assertIn(2, data["hotels"]["H1"]["reserved_rooms"])

    def test_create_duplicate_raises(self) -> None:
        """Creating a reservation with a duplicate ID raises ValueError."""
        Reservation("R1", "C1", "H1", [1], "2026-03-01", "2026-03-05").create()
        with self.assertRaises(ValueError):
            Reservation(
                "R1", "C1", "H1", [2], "2026-03-01", "2026-03-05"
            ).create()

    def test_create_customer_not_found_raises(self) -> None:
        """Creating a reservation with unknown customer raises ValueError."""
        with self.assertRaises(ValueError):
            Reservation(
                "R1", "UNKNOWN", "H1", [1], "2026-03-01", "2026-03-05"
            ).create()

    def test_create_hotel_not_found_raises(self) -> None:
        """Creating a reservation with unknown hotel raises ValueError."""
        with self.assertRaises(ValueError):
            Reservation(
                "R1", "C1", "UNKNOWN", [1], "2026-03-01", "2026-03-05"
            ).create()

    def test_cancel(self) -> None:
        """cancel() removes the reservation and frees the rooms."""
        Reservation("R1", "C1", "H1", [1, 2], "2026-03-01",
                    "2026-03-05").create()
        Reservation.cancel("R1")
        data = _load()
        self.assertNotIn("R1", data["reservations"])
        self.assertNotIn(1, data["hotels"]["H1"]["reserved_rooms"])
        self.assertNotIn(2, data["hotels"]["H1"]["reserved_rooms"])

    def test_cancel_not_found_raises(self) -> None:
        """Cancelling a non-existent reservation raises ValueError."""
        with self.assertRaises(ValueError):
            Reservation.cancel("UNKNOWN")


if __name__ == "__main__":
    unittest.main()

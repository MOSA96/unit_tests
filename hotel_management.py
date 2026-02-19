"""Hotel management system."""

import json
import os
from typing import Optional
from dataclasses import dataclass, field

JSON_FILE = "hotel.json"


def _load() -> dict:
    """Load data from JSON file."""
    if not os.path.exists(JSON_FILE):
        return {"hotels": {}, "customers": {}, "reservations": {}}
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    """Write data to JSON file."""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


class Customer:
    """Custormer for hotel."""

    def __init__(self, customer_id: str, name: str, email: str) -> None:
        """Create customer entity."""
        self.customer_id = customer_id
        self.name = name
        self.email = email

    def create(self) -> None:
        """Create customer and save on JSON."""
        data = _load()
        if self.customer_id in data["customers"]:
            raise ValueError(f"Customer {self.customer_id} already exists.")

        data["customers"][self.customer_id] = {
            "name": self.name,
            "email": self.email
        }

        _save(data)

    @staticmethod
    def delete(customer_id: str) -> None:
        """Delete customer using ID."""
        data = _load()
        if customer_id not in data["customers"]:
            raise ValueError(f"Customer {customer_id} not found.")

        del data["customers"][customer_id]
        _save(data)

    @staticmethod
    def display_customer_info(customer_id: str) -> None:
        """Print customer info using ID."""
        data = _load()
        if customer_id not in data["customers"]:
            raise ValueError(f"Customer {customer_id} not found.")

        print(data["customers"][customer_id])

    @staticmethod
    def modify(
        customer_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None
    ) -> None:
        """Update the name, or email of a customer by ID."""
        data = _load()
        if customer_id not in data["customers"]:
            raise ValueError(f"Customer {customer_id} not found.")
        if name:
            data["customers"][customer_id]["name"] = name
        if email:
            data["customers"][customer_id]["email"] = email
        _save(data)


@dataclass(slots=True)
class Reservation:
    """Reservation linking a customer to hotel."""
    reservation_id: str
    customer_id: str
    hotel_id: str
    rooms: list[int] = field(default_factory=list)
    check_in: str = ""
    check_out: str = ""

    def create(self) -> None:
        """Create reservation and save on JSON."""
        data = _load()
        if self.reservation_id in data["reservations"]:
            raise ValueError(
                f"Reservation {self.reservation_id} already exists."
            )
        if self.customer_id not in data["customers"]:
            raise ValueError(f"Customer {self.customer_id} not found.")
        if self.hotel_id not in data["hotels"]:
            raise ValueError(f"Hotel {self.hotel_id} not found.")

        for room in self.rooms:
            Hotel.reserve_room(self.hotel_id, room)
            data = _load()

        data["reservations"][self.reservation_id] = {
            "customer_id": self.customer_id,
            "hotel_id": self.hotel_id,
            "rooms": self.rooms,
            "check_in": self.check_in,
            "check_out": self.check_out
        }
        _save(data)

    @staticmethod
    def cancel(reservation_id: str) -> None:
        """Cancel a reservation."""
        data = _load()
        if reservation_id not in data["reservations"]:
            raise ValueError(f"Reservation {reservation_id} not found.")
        reservation = data["reservations"][reservation_id]

        for room in reservation["rooms"]:
            Hotel.cancel_room(reservation["hotel_id"], room)

        data = _load()
        del data["reservations"][reservation_id]
        _save(data)


class Hotel:
    """Hotel with a set of rooms."""

    def __init__(self, hotel_id: str, name: str, total_rooms: int) -> None:
        """Create hotel entity."""
        self.hotel_id = hotel_id
        self.name = name
        self.total_rooms = total_rooms

    def create(self) -> None:
        """Create hotel and save on JSON."""
        data = _load()
        if self.hotel_id in data["hotels"]:
            raise ValueError(f"Hotel {self.hotel_id} already exists.")

        data["hotels"][self.hotel_id] = {
            "name": self.name,
            "total_rooms": self.total_rooms,
            "reserved_rooms": []
        }

        _save(data)

    @staticmethod
    def delete(hotel_id: str) -> None:
        """Delete hotel using ID."""
        data = _load()
        if hotel_id not in data["hotels"]:
            raise ValueError(f"hotel {hotel_id} not found.")

        del data["hotels"][hotel_id]
        _save(data)

    @staticmethod
    def display_hotel_info(hotel_id: str) -> None:
        """Print hotel info using ID."""
        data = _load()
        if hotel_id not in data["hotels"]:
            raise ValueError(f"hotel {hotel_id} not found.")

        print(data["hotels"][hotel_id])

    @staticmethod
    def modify(
        hotel_id: str,
        name: Optional[str] = None,
        total_rooms: Optional[int] = None
    ) -> None:
        """Update the name, total rooms of a hotel by ID."""
        data = _load()
        if hotel_id not in data["hotels"]:
            raise ValueError(f"Hotel {hotel_id} not found.")
        if name:
            data["hotels"][hotel_id]["name"] = name
        if total_rooms:
            data["hotels"][hotel_id]["total_rooms"] = total_rooms
        _save(data)

    @staticmethod
    def reserve_room(hotel_id: str, room_number: int) -> None:
        """Reserved room in a hotel."""
        data = _load()
        if hotel_id not in data["hotels"]:
            raise ValueError(f"Hotel {hotel_id} not found.")

        hotel = data["hotels"][hotel_id]

        if room_number > hotel["total_rooms"]:
            raise ValueError(f"Room {room_number} does not exist.")

        if room_number in hotel["reserved_rooms"]:
            raise ValueError(f"Room {room_number} is already reserved.")

        hotel["reserved_rooms"].append(room_number)
        _save(data)

    @staticmethod
    def cancel_room(hotel_id: str, room_number: int) -> None:
        """Mark a single room as available in a hotel."""
        data = _load()
        if hotel_id not in data["hotels"]:
            raise ValueError(f"Hotel {hotel_id} not found.")
        hotel = data["hotels"][hotel_id]
        if room_number not in hotel["reserved_rooms"]:
            raise ValueError(f"Room {room_number} is not reserved.")
        hotel["reserved_rooms"].remove(room_number)
        _save(data)

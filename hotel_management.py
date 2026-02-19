"""Hotel management system."""

import json
import os
from typing import Optional


JSON_FILE = "hotel.json"

def _load() -> dict:
    """Load data from JSON file."""
    if not os.path.exists(JSON_FILE):
        return {"hotels": {}, "customers": {}, "reservations": {}}
    with open(JSON_FILE, "r") as f:
        return json.load(f)


def _save(JSON_FILE: str, data: dict) -> None:
    """Write data to JSON file."""
    with open(JSON_FILE, "w") as f:
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



class Reservation:
    """Reservation linking a customer to hotel rooms."""
    pass


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
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
    pass


class Hotel:
    pass
"""Script to load a JSON test file, run all hotel operations, and save."""

import argparse
import json
import os
import shutil
from hotel_management import Customer, Hotel, Reservation, JSON_FILE


def load_input(path: str) -> dict:
    """Load and return the JSON data from the given file path."""
    with open(path, "r") as f:
        return json.load(f)


def run_customers(customers: dict) -> None:
    """Create, display, modify, and delete each customer in the input."""
    for customer_id, info in customers.items():
        name = str(info.get("name", ""))
        email = str(info.get("email", ""))

        try:
            Customer(customer_id, name, email).create()
            print(f"  [OK] Created customer {customer_id}")
        except ValueError as e:
            print(f"  [FAIL] Create customer {customer_id}: {e}")
            continue

        try:
            Customer.display_customer_info(customer_id)
            print(f"  [OK] Displayed customer {customer_id}")
        except ValueError as e:
            print(f"  [FAIL] Display customer {customer_id}: {e}")

        try:
            Customer.modify(customer_id, name=name + " (modified)")
            print(f"  [OK] Modified customer {customer_id}")
        except ValueError as e:
            print(f"  [FAIL] Modify customer {customer_id}: {e}")


def run_hotels(hotels: dict) -> None:
    """Create, display, modify, and reserve rooms for each hotel in input."""
    for hotel_id, info in hotels.items():
        name = info.get("name", "")
        total_rooms = info.get("total_rooms", 0)

        try:
            Hotel(hotel_id, name, total_rooms).create()
            print(f"  [OK] Created hotel {hotel_id}")
        except ValueError as e:
            print(f"  [FAIL] Create hotel {hotel_id}: {e}")
            continue

        try:
            Hotel.display_hotel_info(hotel_id)
            print(f"  [OK] Displayed hotel {hotel_id}")
        except ValueError as e:
            print(f"  [FAIL] Display hotel {hotel_id}: {e}")

        try:
            Hotel.modify(hotel_id, name=name + " (modified)")
            print(f"  [OK] Modified hotel {hotel_id}")
        except ValueError as e:
            print(f"  [FAIL] Modify hotel {hotel_id}: {e}")

        for room in info.get("reserved_rooms", []):
            try:
                Hotel.reserve_room(hotel_id, room)
                print(f"  [OK] Reserved room {room} in hotel {hotel_id}")
            except ValueError as e:
                print(f"  [FAIL] Reserve room {room} in hotel {hotel_id}: {e}")

def run_reservations(reservations: dict) -> None:
    """Create and cancel each reservation in the input."""
    for reservation_id, info in reservations.items():
        customer_id = info.get("customer_id", "")
        hotel_id = info.get("hotel_id", "")
        rooms = info.get("rooms", [])
        check_in = info.get("check_in", "")
        check_out = info.get("check_out", "")

        try:
            Reservation(
                reservation_id, customer_id, hotel_id,
                rooms, check_in, check_out
            ).create()
            print(f"  [OK] Created reservation {reservation_id}")
        except ValueError as e:
            print(f"  [FAIL] Create reservation {reservation_id}: {e}")
            continue

        try:
            Reservation.cancel(reservation_id)
            print(f"  [OK] Cancelled reservation {reservation_id}")
        except ValueError as e:
            print(f"  [FAIL] Cancel reservation {reservation_id}: {e}")

def run_deletes(data: dict) -> None:
    """Delete all customers and hotels that were successfully created."""
    for customer_id in data.get("customers", {}):
        try:
            Customer.delete(customer_id)
            print(f"  [OK] Deleted customer {customer_id}")
        except ValueError as e:
            print(f"  [FAIL] Delete customer {customer_id}: {e}")

    for hotel_id in data.get("hotels", {}):
        try:
            Hotel.delete(hotel_id)
            print(f"  [OK] Deleted hotel {hotel_id}")
        except ValueError as e:
            print(f"  [FAIL] Delete hotel {hotel_id}: {e}")

def main() -> None:
    """Run all operations."""

    parser = argparse.ArgumentParser(
        description="Run hotel management operations from a JSON input file."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input JSON file (e.g. test_valid.json)"
    )
    parser.add_argument(
        "--output",
        default="output.json",
        help="Path to the output JSON file (default: output.json)"
    )
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        print(f"[ERROR] File not found: {args.input_file}")
        return

    if os.path.exists(JSON_FILE):
        os.remove(JSON_FILE)

    data = load_input(args.input_file)

    print("\n--- Customers ---")
    run_customers(data.get("customers", {}))

    print("\n--- Hotels ---")
    run_hotels(data.get("hotels", {}))

    print("\n--- Reservations ---")
    run_reservations(data.get("reservations", {}))

    print("\n--- Deletes ---")
    run_deletes(data)

    shutil.copy(JSON_FILE, args.output)
    print(f"\n[DONE] Final data saved to {args.output}")


if __name__ == "__main__":
    main()
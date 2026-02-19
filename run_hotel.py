"""Script to load a JSON test file, run all hotel operations, and save."""

import json


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
            Customer.display(customer_id)
            print(f"  [OK] Displayed customer {customer_id}")
        except ValueError as e:
            print(f"  [FAIL] Display customer {customer_id}: {e}")

        try:
            Customer.modify(customer_id, name=name + " (modified)")
            print(f"  [OK] Modified customer {customer_id}")
        except ValueError as e:
            print(f"  [FAIL] Modify customer {customer_id}: {e}")

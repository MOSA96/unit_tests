import json
import os


def _load(filename: str) -> dict:
    if not os.path.exists(filename):
        return {"hotels": {}, "customers": {}, "reservations": {}}
    with open(filename, "r") as f:
        return json.load(f)


def _save(filename: str, data: dict) -> None:
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)



class Customer:
    pass


class Reservation:
    pass


class Hotel:
    pass
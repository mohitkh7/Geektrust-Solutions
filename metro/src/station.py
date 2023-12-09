from collections import defaultdict
from src.common.exceptions import InsufficientBalanceException
from src.card import MetroCard, CardGateway
from src.common.enums import Passenger


class StationPassengerCount:
    """Count the number of passenger who check-in in a station"""

    def __init__(self):
        self._passenger_count = defaultdict(int)

    def check_in(self, passenger_type):
        self._passenger_count[passenger_type] += 1

    def summary(self) -> str:
        result = "PASSENGER_TYPE_SUMMARY\n"
        sorted_count = sorted(self._passenger_count.items(), key=lambda x: (-1 * x[1], x[0].value))
        arr = [f"{ptype.value} {count}" for ptype, count in sorted_count]
        return result + ("\n").join(arr)


class StationCollection:
    """Collect statistics of charges and discount"""
    def __init__(self):
        self._charges = 0
        self._discount = 0

    @property
    def charges(self) -> int:
        return self._charges

    def collect_charge(self, charge: int):
        self._charges += charge

    @property
    def discount(self) -> int:
        return self._discount

    def collect_discount(self, amount: int):
        self._discount += amount

    def summary(self, station_name) -> str:
        return f"TOTAL_COLLECTION {station_name} {self._charges} {self._discount}"


class Station:
    def __init__(self, name, biller, card_gateway, passenger_count, collection):
        self._name = name
        self._biller = biller
        self._card_gateway = card_gateway
        self._passenger_count = passenger_count
        self._collection = collection

    def check_in(self, card: MetroCard, passenger_type: Passenger):
        trip_charge, trip_discount = self._biller.calculate_cost(card.number, passenger_type)
        service_charge = self._card_gateway.charge(card, trip_charge)
        self._collection.collect_charge(trip_charge)
        self._collection.collect_charge(service_charge)
        self._collection.collect_discount(trip_discount)
        self._passenger_count.check_in(passenger_type)

    def summary(self):
        collection_summary = self._collection.summary(self._name)
        passenger_summary = self._passenger_count.summary()
        return collection_summary + "\n" + passenger_summary

from src.common.enums import Passenger
from src.common.constants import DEFAULT_DISCOUNT

class Journey:
    def __init__(self):
        self._card_history = set()

    def add_journey(self, card_number):
        self._card_history.add(card_number)

    def remove_journey(self, card_number):
        self._card_history.remove(card_number)

    def is_return_journey(self, card_number):
        return card_number in self._card_history


class Pricing:
    def __init__(self, discount_percentage):
        self._discount_percentage = discount_percentage
        self._charges = {}

    def set_charge(self, passenger_type, charge):
        self._charges[passenger_type] = charge

    def calculate_single_journey_cost(self, passenger_type) -> (int, int):
        return self._charges[passenger_type], DEFAULT_DISCOUNT

    def calculate_return_journey_cost(self, passenger_type) -> (int, int):
        cost = self._charges.get(passenger_type)
        discount = int(cost * self._discount_percentage)
        return cost - discount, discount


class Billing:
    def __init__(self, journey, pricing):
        self._journey = journey
        self._pricing = pricing

    def calculate_cost(self, card_number, passenger_type) -> (int, int):
        if self._journey.is_return_journey(card_number):
            self._journey.remove_journey(card_number)
            return self._pricing.calculate_return_journey_cost(passenger_type)
        else:
            self._journey.add_journey(card_number)
            return self._pricing.calculate_single_journey_cost(passenger_type)

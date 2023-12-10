from src.common.exceptions import InsufficientBalanceException
from src.common.constants import MIN_RECHARGE_AMOUNT


class MetroCard:

    def __init__(self, number: str, balance: int):
        self._number = number
        self._balance = balance

    def withdraw(self, charge: int):
        if charge > self._balance:
            raise InsufficientBalanceException(self._number, charge - self._balance)
        self._balance -= charge

    def recharge(self, amount: int):
        if amount < MIN_RECHARGE_AMOUNT:
            raise ValueError("Recharge amount must be a non-negative value.")
        self._balance += amount

    @property
    def number(self):
        return self._number

    @property
    def balance(self):
        return self._balance


class CardGateway:
    """manages interaction with a card"""
    def __init__(self, perc):
        self._service_charge_perc = perc

    def charge(self, card, amount) -> int:
        service_charge = 0
        try:
            card.withdraw(amount)
        except InsufficientBalanceException as exc:
            card.recharge(exc.diff)
            card.withdraw(amount)
            service_charge = int(exc.diff * self._service_charge_perc)
        return service_charge

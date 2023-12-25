"""Asset class such as Equity, Debt, Gold etc."""
from math import floor

PERC = 100


class Asset:
    def __init__(self, name, history):
        self._name = name
        self._history = history
        self._amount = 0.0
        self._sip = None

    def set_sip(self, sip):
        self._sip = sip

    def set_amount(self, month, amount):
        self._amount = floor(amount)
        self._history.set(month, amount)

    def get_amount(self, month):
        return self._history.get(month)

    def _do_sip(self, month):
        sip_amount = self._sip.get(month)
        self.set_amount(month, self._amount + sip_amount)

    def apply_monthly_change(self, month, change_perc):
        self._do_sip(month)
        perc = float(change_perc.rstrip("%"))
        diff = floor((self._amount * perc) / PERC)
        self.set_amount(month, self._amount + diff)

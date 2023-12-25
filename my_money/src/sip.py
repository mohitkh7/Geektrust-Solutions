from math import floor
from src.common.enums import Months

NON_SIP_MONTH = [Months.JANUARY]
DEFAULT_SIP_AMOUNT = 0


class SIP:
    def __init__(self, amount):
        self.set(amount)

    def set(self, amount):
        self._sip_amount = floor(float(amount))

    def get(self, month):
        return self._sip_amount if month not in NON_SIP_MONTH else DEFAULT_SIP_AMOUNT

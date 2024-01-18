from src.asset import Asset
from src.sip import SIP
from src.history import History
from src.common.enums import Months


class Portfolio:
    def __init__(self):
        self._equity = Asset('Equity', History())
        self._debt = Asset('Debt', History())
        self._gold = Asset('Gold', History())
        self._rebalance_history = None

    def allocate(self, equity_amount, debt_amount, gold_amount):
        self._equity.set_amount(Months.JANUARY, equity_amount, )
        self._debt.set_amount(Months.JANUARY, debt_amount)
        self._gold.set_amount(Months.JANUARY, gold_amount)
        total = equity_amount + debt_amount + gold_amount
        self._ratio = (
            equity_amount / total,
            debt_amount / total,
            gold_amount / total)

    def sip(self, equity_amount, debt_amount, gold_amount):
        self._equity.set_sip(SIP(equity_amount))
        self._debt.set_sip(SIP(debt_amount))
        self._gold.set_sip(SIP(gold_amount))

    def change(self, equity_perc, debt_perc, gold_perc, month):
        month = Months[month]  # get enum repr for month
        self._equity.apply_monthly_change(month, equity_perc)
        self._debt.apply_monthly_change(month, debt_perc)
        self._gold.apply_monthly_change(month, gold_perc)
        if month in (Months.JUNE, Months.DECEMBER):
            self.rebalance(month)

    def balance(self, month):
        if isinstance(month, str):
            month = Months[month]
        return (
            self._equity.get_amount(month),
            self._debt.get_amount(month),
            self._gold.get_amount(month))

    def rebalance(self, month):
        total = sum(self.balance(month))
        self._equity.set_amount(month, total * self._ratio[0])
        self._debt.set_amount(month, total * self._ratio[1])
        self._gold.set_amount(month, total * self._ratio[2])
        self._rebalance_history = self.balance(month)

    def get_rebalance(self):
        return self._rebalance_history if self._rebalance_history else ['CANNOT_REBALANCE']

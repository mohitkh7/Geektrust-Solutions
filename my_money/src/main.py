from src.portfolio import Portfolio
from src.common.enums import Command


class MyMoneyManager:
    def __init__(self):
        self._portfolio = Portfolio()

    def execute(self, instructions):
        for instruction in instructions:
            instruction = instruction.strip()
            args = instruction.split(" ")
            if args[0] == Command.ALLOCATE.value:
                self._portfolio.allocate(*map(int, args[1:]))
            elif args[0] == Command.SIP.value:
                self._portfolio.sip(*args[1:])
            elif args[0] == Command.CHANGE.value:
                self._portfolio.change(*args[1:])
            elif args[0] == Command.BALANCE.value:
                result = self._portfolio.balance(*args[1:])
                print(*result)
            elif args[0] == Command.REBALANCE.value:
                result = self._portfolio.get_rebalance()
                print(*result)
            else:
                raise ValueError(f"Unknown instruction found: {args[0]}")

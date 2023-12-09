"""custom exceptions"""

class InsufficientBalanceException(Exception):
    def __init__(self, card_number, diff):
        super().__init__(f"Insufficient Balance in card: {card_number}. Please Recharge")
        self.diff = diff

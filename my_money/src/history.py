"""To save amount history"""
from math import floor


class History:
    def __init__(self):
        self._history = {}

    def set(self, month, amount):
        self._history[month] = floor(amount)

    def get(self, month):
        return self._history.get(month)

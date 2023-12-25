import unittest
from src.history import History
from src.common.enums import Months


class TestHistory(unittest.TestCase):
    def test_get_history(self):
        history = History()
        history.set(Months.MAY, 100)
        self.assertEqual(history.get(Months.MAY), 100)

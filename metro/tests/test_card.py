import unittest
from unittest.mock import Mock
from src.card import MetroCard, CardGateway
from src.common.exceptions import InsufficientBalanceException


class TestMetroCard(unittest.TestCase):
    def setUp(self):
        self.card = MetroCard("test_card", 100)

    def test_number(self):
        self.assertEqual(self.card.number, "test_card")

    def test_card_balance(self):
        self.assertEqual(self.card.balance, 100)

    def test_positive_recharge(self):
        self.card.recharge(135)
        self.assertEqual(self.card.balance, 235)

    def test_negative_recharge(self):
        with self.assertRaises(ValueError) as context:
            self.card.recharge(-50)

    def test_withdraw_with_sufficient_balance(self):
        self.card.withdraw(25)
        self.assertEqual(self.card.balance, 75)

    def test_withdraw_with_insufficient_balance(self):
        with self.assertRaises(InsufficientBalanceException) as context:
            self.card.withdraw(135)
        self.assertEqual(context.exception.diff, 35)


class TestCardGateway(unittest.TestCase):
    def setUp(self):
        self.service_charge_perc = 0.02
        self.card_gw = CardGateway(self.service_charge_perc)
        self.card = Mock()

    def test_charge_with_sufficient_balance(self):
        self.card.withdraw.return_value = None

        service_charge = self.card_gw.charge(self.card, 100)

        self.assertEqual(service_charge, 0)
        self.card.withdraw.assert_called_once_with(100)

    def test_charge_with_insufficient_balance(self):
        self.card.withdraw.side_effect = [InsufficientBalanceException("test_card", 100), None]

        service_charge = self.card_gw.charge(self.card, 300)

        self.assertEqual(service_charge, 2)
        self.card.recharge.assert_called_once_with(100)
        self.card.withdraw.assert_called_with(300)
        self.card.withdraw.assert_called_with(300)
import unittest
from unittest.mock import Mock

from src.invoice import Invoice
from src.common.enums import Programme, CouponName
from src.common.constants import PRO_MEMBERSHIP_FEE


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.mock_orders = Mock()
        self.mock_coupon_discount = Mock()
        self.invoice = Invoice(self.mock_orders, self.mock_coupon_discount)

    def set_membership_fee(self):
        self.assertEqual(self.invoice.membership_fee, 0)
        self.invoice.membership_fee = 500
        self.assertEqual(self.invoice.membership_fee, 500)

    def test_compute(self):
        self.mock_orders.total_final_cost = 800
        self.mock_orders.total_membership_discount = 200
        self.mock_coupon_discount.apply.return_value = ("NONE", 100)

        self.invoice.compute()

        self.assertEqual(self.invoice.total, 1200)

    def test_get_bill(self):
        self.mock_orders.total_final_cost = 800
        self.mock_orders.total_membership_discount = 200
        self.mock_coupon_discount.apply.return_value = ("NONE", 100)

        self.invoice.compute()

        self.assertGreater(len(self.invoice.get_bill()), 100)

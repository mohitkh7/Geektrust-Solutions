import unittest
from unittest.mock import Mock

from src.main import GeekAcademy
from src.common.enums import Programme, CouponName
from src.common.constants import PRO_MEMBERSHIP_FEE


class TestGeekAcademy(unittest.TestCase):
    def setUp(self):
        self.academy = GeekAcademy()

    def test_add_pro_membership(self):
        self.academy.membership = Mock()
        self.academy.invoice = Mock()
        instructions = ["ADD_PRO_MEMBERSHIP"]

        self.academy.execute(instructions)

        self.academy.membership.add_pro_membership.assert_called()
        self.assertEqual(self.academy.invoice.membership_fee, PRO_MEMBERSHIP_FEE)

    def test_print_bill(self):
        self.academy.membership = Mock()
        self.academy.invoice = Mock()
        self.academy.invoice.get_bill.return_value = ''
        instructions = ["PRINT_BILL"]

        self.academy.execute(instructions)

        self.academy.invoice.compute.assert_called()
        self.academy.invoice.get_bill.assert_called()

    def test_apply_coupan_deal_g20(self):
        self.academy.deal_g20 = Mock()
        instructions = ["APPLY_COUPON DEAL_G20"]

        self.academy.execute(instructions)

        self.academy.deal_g20.activate.assert_called()


    def test_apply_coupan_deal_g5(self):
        self.academy.deal_g5 = Mock()
        instructions = ["APPLY_COUPON DEAL_G5"]

        self.academy.execute(instructions)

        self.academy.deal_g5.activate.assert_called()

    def test_apply_unknown_coupan(self):
        self.academy.orders = Mock()
        instructions = ["APPLY_COUPON UNKNOWN"]

        with self.assertRaises(ValueError):
            self.academy.execute(instructions)

    def test_add_programme(self):
        self.academy.orders = Mock()
        instructions = ["ADD_PROGRAMME CERTIFICATION 3"]

        self.academy.execute(instructions)

        self.academy.orders.add_programme.assert_called_once_with(Programme.CERTIFICATION, 3)

    def test_add_unknown_programme(self):
        self.academy.orders = Mock()
        instructions = ["ADD_PROGRAMME UNKNOWN 3"]

        with self.assertRaises(ValueError):
            self.academy.execute(instructions)

    def test_unknown_instruction(self):
        instructions = ["UNKNOWN_INSTRUCTION 3"]

        with self.assertRaises(ValueError):
            self.academy.execute(instructions)

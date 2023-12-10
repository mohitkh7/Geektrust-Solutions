import unittest
from unittest.mock import Mock

from src.order import Order, OrderContainer
from src.common.enums import Programme


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.fee = Mock()
        self.test_qty = 2
        self.order = Order(self.fee, Programme.CERTIFICATION, self.test_qty)

    def test_quantity(self):
        self.assertEqual(self.order.quantity, 2)

    def test_actual_cost(self):
        self.fee.get_actual_cost.return_value = 3000
        self.assertEqual(self.order.actual_cost, 3000)

    def test_membership_discount(self):
        self.fee.get_actual_cost.return_value = 1000
        self.fee.get_members_discount.return_value = 0.2
        self.assertEqual(self.order.membership_discount, 200)

    def test_final_cost(self):
        self.fee.get_actual_cost.return_value = 1000
        self.fee.get_members_discount.return_value = 0.2
        self.assertEqual(self.order.final_cost, 800)

    def test_total_actual_cost(self):
        self.fee.get_actual_cost.return_value = 3000
        self.assertEqual(self.order.total_actual_cost, 3000 * self.test_qty)

    def test_total_membership_discount(self):
        self.fee.get_actual_cost.return_value = 1000
        self.fee.get_members_discount.return_value = 0.2
        self.assertEqual(self.order.total_membership_discount, 200 * self.test_qty)

    def test_total_final_cost(self):
        self.fee.get_actual_cost.return_value = 1000
        self.fee.get_members_discount.return_value = 0.2
        self.assertEqual(self.order.total_final_cost, 800 * self.test_qty)


class TestOrderContainer(unittest.TestCase):
    def setUp(self):
        self.fee = Mock()
        self.orders = OrderContainer(self.fee)

    def test_total_quantity_with_no_order(self):
        self.assertEqual(self.orders.total_quantity, 0)

    def test_total_quantity_with_order(self):
        self.orders.add_programme(Programme.CERTIFICATION, 5)
        self.orders.add_programme(Programme.DIPLOMA, 3)
        self.assertEqual(self.orders.total_quantity, 8)

    def test_total_final_cost(self):
        self.fee.get_actual_cost.return_value = 1000
        self.fee.get_members_discount.return_value = 0.5
        self.orders.add_programme(Programme.CERTIFICATION, 5)
        self.orders.add_programme(Programme.DIPLOMA, 3)
        self.assertEqual(self.orders.total_final_cost, 4000.0)

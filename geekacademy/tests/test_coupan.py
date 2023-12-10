import unittest
from unittest.mock import Mock

from src.coupon import B4G1, DEAL_G20, DEAL_G5, CouponDiscount
from src.common.enums import Programme, CouponName


class TestB4G1(unittest.TestCase):
    def setUp(self):
        self.coupan = B4G1()
        self.orders = Mock()

    def test_name(self):
        self.assertEqual(self.coupan.name, CouponName.B4G1.value)

    def test_should_be_active_by_default(self):
        self.assertTrue(self.coupan.is_active())

    def test_should_be_applicable_above_threshold_quantity(self):
        self.orders.total_quantity = 5
        self.assertTrue(self.coupan.is_applicable(self.orders, 1000))

    def test_should_not_be_applicable_below_threshold_quantity(self):
        self.orders.total_quantity = 2
        self.assertFalse(self.coupan.is_applicable(self.orders, 1000))        

    def test_should_discount_lowest_cost_programme(self):
        self.orders.lowest_priced_programme_cost = 2500
        self.assertEqual(self.coupan.discount_amount(self.orders, 1000), 2500)


class TestDeal_G20(unittest.TestCase):
    def setUp(self):
        self.coupan = DEAL_G20()
        self.orders = Mock()

    def test_name(self):
        self.assertEqual(self.coupan.name, CouponName.DEAL_G20.value)

    def test_should_be_inactive_by_default(self):
        self.assertFalse(self.coupan.is_active())

    def test_should_be_applicable_above_threshold_total(self):
        self.coupan.activate()
        self.assertTrue(self.coupan.is_applicable(self.orders, 12000))

    def test_should_not_be_applicable_below_threshold_total(self):
        self.assertFalse(self.coupan.is_applicable(self.orders, 9900))        

    def test_should_discount_20_percent(self):
        self.coupan.activate()
        self.assertEqual(self.coupan.discount_amount(self.orders, 20000), 4000)


class TestDeal_G5(unittest.TestCase):
    def setUp(self):
        self.coupan = DEAL_G5()
        self.orders = Mock()

    def test_name(self):
        self.assertEqual(self.coupan.name, CouponName.DEAL_G5.value)

    def test_should_be_inactive_by_default(self):
        self.assertFalse(self.coupan.is_active())

    def test_should_be_applicable_above_threshold_quantity(self):
        self.coupan.activate()
        self.orders.total_quantity = 3
        self.assertTrue(self.coupan.is_applicable(self.orders, 10000))

    def test_should_not_be_applicable_below_threshold_total(self):
        self.orders.total_quantity = 1
        self.assertFalse(self.coupan.is_applicable(self.orders, 10000))        

    def test_should_discount_5_percent(self):
        self.coupan.activate()
        self.orders.total_quantity = 3
        self.assertEqual(self.coupan.discount_amount(self.orders, 10000), 500)


class TestCouponDiscount(unittest.TestCase):
    def setUp(self):
        self.b4g1 = Mock()
        self.deal_g20 = Mock()
        self.deal_g5 = Mock()
        self.orders = Mock()

        self.b4g1.name = CouponName.B4G1.name
        self.deal_g20.name = CouponName.DEAL_G20.name
        self.deal_g5.name = CouponName.DEAL_G5.name

        self.b4g1.is_applicable.return_value = False
        self.deal_g20.discount_amount.return_value = 0
        self.deal_g5.discount_amount.return_value = 0
        self.coupon_discount = CouponDiscount(self.b4g1, self.deal_g20, self.deal_g5)

    def test_when_no_coupon_applicable(self):
        result = self.coupon_discount.apply(self.orders, 12000)
        self.assertEqual(result[0], "NONE")
        self.assertEqual(result[1], 0)

    def test_when_b4g1_applicable(self):
        self.b4g1.is_applicable.return_value = True
        self.b4g1.discount_amount.return_value = 1000

        result = self.coupon_discount.apply(self.orders, 12000)

        self.assertEqual(result, (CouponName.B4G1.value, 1000))

    def test_when_deal_g20_applicable(self):
        self.deal_g20.is_applicable.return_value = True
        self.deal_g20.discount_amount.return_value = 1000

        result = self.coupon_discount.apply(self.orders, 12000)

        self.assertEqual(result, (CouponName.DEAL_G20.value, 1000))

    def test_when_deal_g5_applicable(self):
        self.deal_g5.is_applicable.return_value = True
        self.deal_g5.discount_amount.return_value = 1000

        result = self.coupon_discount.apply(self.orders, 12000)

        self.assertEqual(result, (CouponName.DEAL_G5.value, 1000))

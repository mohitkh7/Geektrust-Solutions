import unittest
from unittest.mock import Mock
from src.billing import Journey, Pricing, Billing

from src.common.enums import Passenger


class TestJourney(unittest.TestCase):
    def setUp(self):
        self.journey = Journey()

    def test_add_journey(self):
        self.journey.add_journey("test_card")
        self.assertIn("test_card", self.journey._card_history)
        self.assertTrue(self.journey.is_return_journey("test_card"))

    def test_remove_journey(self):
        self.journey.add_journey("test_card")
        self.journey.remove_journey("test_card")
        self.assertNotIn("test_card", self.journey._card_history)
        self.assertFalse(self.journey.is_return_journey("test_card"))

    def test_is_return_journey(self):
        self.assertFalse(self.journey.is_return_journey("non-existent"))

        self.journey.add_journey("test_card")
        self.assertTrue(self.journey.is_return_journey("test_card"))


class TestPricing(unittest.TestCase):
    def setUp(self):
        self.pricing = Pricing(0.5)
        self.pricing.set_charge(Passenger.Adult, 200)

    def test_set_charge(self):
        self.pricing.set_charge(Passenger.Kid, 50)
        self.assertIn(Passenger.Kid, self.pricing._charges)

    def test_calculate_single_journey_cost(self):
        cost, discount = self.pricing.calculate_single_journey_cost(Passenger.Adult)
        self.assertEqual(cost, 200)
        self.assertEqual(discount, 0)

    def test_calculate_return_journey_cost(self):
        cost, discount = self.pricing.calculate_return_journey_cost(Passenger.Adult)
        self.assertEqual(cost, 100)
        self.assertEqual(discount, 100)


class TestBilling(unittest.TestCase):
    def setUp(self):
    	self.journey = Mock()
    	self.pricing = Mock()
    	self.billing = Billing(self.journey, self.pricing)

    def test_calculate_single_journey_cost(self):
        self.journey.is_return_journey.return_value = False
        self.pricing.calculate_single_journey_cost.return_value = (200, 0)

        result = self.billing.calculate_cost("test_card", Passenger.Adult)

        self.assertEqual(result, (200, 0))
        self.journey.add_journey.assert_called_once_with("test_card")
        self.pricing.calculate_single_journey_cost.assert_called_once_with(Passenger.Adult)

    def test_calculate_return_journey_cost(self):
        self.journey.is_return_journey.return_value = True
        self.pricing.calculate_return_journey_cost.return_value = (50, 50)

        result = self.billing.calculate_cost("test_card", Passenger.Kid)

        self.assertEqual(result, (50, 50))
        self.journey.remove_journey.assert_called_once_with("test_card")
        self.pricing.calculate_return_journey_cost.assert_called_once_with(Passenger.Kid)

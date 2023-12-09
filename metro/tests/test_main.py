import unittest
from unittest.mock import Mock
from src.main import MetroCardManager, RETURN_TRIP_DISCOUNT, SERVICE_CHARGE_PERC
from src.card import MetroCard
from src.common.enums import Passenger


class TestMetroCardManager(unittest.TestCase):
    def setUp(self):
        self.metro_card_manager = MetroCardManager()
        self.metro_card_manager.cards = {"card_1": MetroCard("card_1", 100)}

    def test_create_card(self):
        instructions = ["BALANCE card_1 100", "BALANCE card_2 50"]

        self.metro_card_manager.execute(instructions)

        self.assertIn("card_1", self.metro_card_manager.cards)
        self.assertEqual(self.metro_card_manager.cards["card_1"].balance, 100)
        self.assertIn("card_2", self.metro_card_manager.cards)
        self.assertEqual(self.metro_card_manager.cards["card_2"].balance, 50)

    def test_check_in_central_station(self):
        self.metro_card_manager.central_station = Mock()
        instructions = ["CHECK_IN card_1 ADULT CENTRAL"]

        self.metro_card_manager.execute(instructions)

        self.metro_card_manager.central_station.check_in.assert_called_once_with(
            self.metro_card_manager.cards["card_1"], Passenger.Adult
        )

    def test_check_in_airport_station(self):
        self.metro_card_manager.airport_station = Mock()
        instructions = ["CHECK_IN card_1 SENIOR_CITIZEN AIRPORT"]

        self.metro_card_manager.execute(instructions)

        self.metro_card_manager.airport_station.check_in.assert_called_once_with(
            self.metro_card_manager.cards["card_1"], Passenger.Senior_Citizen
        )

    def test_print_summary(self):
        instructions = ["PRINT_SUMMARY"]

        self.metro_card_manager.execute(instructions)        

    def test_unknown_instruction(self):
        instructions = ["UNKNOWN_INSTRUCTION card_1"]

        with self.assertRaises(ValueError):
            self.metro_card_manager.execute(instructions)

    def test_unknown_passenger(self):
        instructions = ["CHECK_IN card_1 UNKNOWN CENTRAL"]

        with self.assertRaises(ValueError):
            self.metro_card_manager.execute(instructions)

    def test_unknown_station(self):
        instructions = ["CHECK_IN card_1 ADULT UNKNOWN"]

        with self.assertRaises(ValueError):
            self.metro_card_manager.execute(instructions)

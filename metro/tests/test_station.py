import unittest
from unittest.mock import Mock
from src.common.enums import Passenger
from src.station import StationPassengerCount, StationCollection, Station
from src.card import MetroCard


class TestStationPassengerCount(unittest.TestCase):
    def setUp(self):
        self.passenger_count = StationPassengerCount()

    def test_summary_empty_count(self):
        summary = self.passenger_count.summary()
        self.assertEqual(summary, "PASSENGER_TYPE_SUMMARY\n")


    def test_summary_with_single_passenger(self):
        self.passenger_count.check_in(Passenger.Adult)
        summary = self.passenger_count.summary()
        self.assertEqual(summary, "PASSENGER_TYPE_SUMMARY\nADULT 1")

    def test_summary_with_multiple_passenger(self):
        self.passenger_count.check_in(Passenger.Adult)
        self.passenger_count.check_in(Passenger.Senior_Citizen)
        self.passenger_count.check_in(Passenger.Kid)
        self.passenger_count.check_in(Passenger.Senior_Citizen)
        summary = self.passenger_count.summary()
        expected_summary = "PASSENGER_TYPE_SUMMARY\nSENIOR_CITIZEN 2\nADULT 1\nKID 1"
        self.assertEqual(summary, expected_summary)


class TestStationCollection(unittest.TestCase):
    def setUp(self):
        self.collection = StationCollection()

    def test_collect_charge(self):
        self.collection.collect_charge(100)
        self.assertEqual(self.collection.charges, 100)

    def test_collect_discount(self):
        self.collection.collect_discount(100)
        self.assertEqual(self.collection.discount, 100)

    def test_summary(self):
        self.collection.collect_charge(78)
        self.collection.collect_discount(32)
        actual_summary = self.collection.summary("AIRPORT")
        expected_summary = "TOTAL_COLLECTION AIRPORT 78 32"
        self.assertEqual(actual_summary, expected_summary)


class TestStation(unittest.TestCase):
    def setUp(self):
        self.biller = Mock()
        self.card_gateway = Mock()
        self.passenger_count = Mock()
        self.collection = Mock()
        self.station = Station("TestStation", self.biller, self.card_gateway, self.passenger_count, self.collection)
        self.metro_card = MetroCard("test_card", 200)

    def test_check_in(self):
        self.biller.calculate_cost.return_value = (100, 10)
        self.card_gateway.charge.return_value = 5

        self.station.check_in(self.metro_card, Passenger.Adult)

        self.biller.calculate_cost.assert_called_once_with("test_card", Passenger.Adult)
        self.card_gateway.charge.assert_called_once_with(self.metro_card, 100)
        self.collection.collect_charge.assert_called()
        self.collection.collect_charge.assert_called_with(5)
        self.collection.collect_discount.assert_called_once_with(10)
        self.passenger_count.check_in.assert_called_once_with(Passenger.Adult)

    def test_summary(self):
        self.collection.summary.return_value = "TOTAL_COLLECTION TestStation 200 20"
        self.passenger_count.summary.return_value = "PASSENGER_TYPE_SUMMARY\nAdult 5\nSenior_Citizen 3"

        self.station.summary()

        self.collection.summary.assert_called_once_with("TestStation")
        self.passenger_count.summary.assert_called_once()

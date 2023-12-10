"""common enums"""
from enum import Enum


class Passenger(Enum):
    Adult = "ADULT"
    Senior_Citizen = "SENIOR_CITIZEN"
    Kid = "KID"


class Command(Enum):
    BALANCE = "BALANCE"
    CHECK_IN = "CHECK_IN"
    PRINT_SUMMARY = "PRINT_SUMMARY"


class StationName(Enum):
    AIRPORT = "AIRPORT"
    CENTRAL = "CENTRAL"

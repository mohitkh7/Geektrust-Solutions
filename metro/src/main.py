from src.billing import Billing, Journey, Pricing
from src.card import MetroCard, CardGateway
from src.station import Station, StationPassengerCount, StationCollection
from src.common.enums import Passenger, Command

RETURN_TRIP_DISCOUNT = 0.5  
SERVICE_CHARGE_PERC = 0.02


class MetroCardManager:
    def __init__(self):
        pricing = Pricing(RETURN_TRIP_DISCOUNT)
        pricing.set_charge(Passenger.Adult, 200)
        pricing.set_charge(Passenger.Senior_Citizen, 100)
        pricing.set_charge(Passenger.Kid, 50)

        biller = Billing(Journey(), pricing)
        card_gw = CardGateway(SERVICE_CHARGE_PERC)
        passenger_count = StationPassengerCount()
        collection = StationCollection()

        self.central_station = Station("CENTRAL", biller, card_gw, StationPassengerCount(), StationCollection())
        self.airport_station = Station("AIRPORT", biller, card_gw, StationPassengerCount(), StationCollection())
        self.cards = {}

    def execute(self, instructions):
        for instruction in instructions:
            instruction = instruction.strip()
            args = instruction.split(" ")
            if args[0] == Command.BALANCE:
                self.create_card(*args[1:])
            elif args[0] == Command.CHECK_IN:
                self.check_in(*args[1:])
            elif args[0] == Command.PRINT_SUMMARY:
                self.print_summary()
            else:
                raise ValueError(f"Unknown instruction found: {args[0]}")


    def create_card(self, card_number: str, balance: int):
        self.cards[card_number] = MetroCard(card_number, int(balance))

    def check_in(self, card_number, passenger_type, origin_station):
        card = self.cards[card_number]
        passenger = self.get_passenger(passenger_type)
        if origin_station == "CENTRAL":
            self.central_station.check_in(card, passenger)
        elif origin_station == "AIRPORT":
            self.airport_station.check_in(card, passenger)
        else:
            raise ValueError(f"Unknown origin station found: {origin_station}")

    def get_passenger(self, passenger_type):
        for ptype in Passenger:
            if ptype.value == passenger_type:
                return ptype
        raise ValueError(f"Unknown passenger type found: {passenger_type}")

    def print_summary(self):
        print(self.central_station.summary())
        print(self.airport_station.summary())

from enum import Enum


class Programme(Enum):
    CERTIFICATION = "CERTIFICATION"
    DEGREE = "DEGREE"
    DIPLOMA = "DIPLOMA"


class Command(Enum):
    ADD_PROGRAMME = "ADD_PROGRAMME"
    APPLY_COUPON = "APPLY_COUPON"
    PRINT_BILL = "PRINT_BILL"
    ADD_PRO_MEMBERSHIP = "ADD_PRO_MEMBERSHIP"


class CouponName(Enum):
    B4G1 = "B4G1"
    DEAL_G20 = "DEAL_G20"
    DEAL_G5 = "DEAL_G5"

from abc import ABC, abstractmethod
from src.common.enums import Programme, Command, CouponName
from src.common.constants import *

class Coupon:
    def __init__(self):
        self._name = ""
        self._active = False

    @abstractmethod
    def is_applicable(self) -> bool:
        pass

    @abstractmethod
    def discount_amount(self) -> int:
        pass

    @property
    def name(self) -> str:
        return self._name.value

    def activate(self):
        self._active = True

    def is_active(self) -> bool:
        return self._active


class B4G1(Coupon):
    def __init__(self):
        super().__init__()
        self._name = CouponName.B4G1
        self.activate()

    def is_applicable(self, orders, sub_total):
        return self.is_active() and orders.total_quantity >= COUPON_B4G1_THRESHOLD_QTY

    def discount_amount(self, orders, sub_total):
        return orders.lowest_priced_programme_cost


class DEAL_G20(Coupon):
    def __init__(self):
        super().__init__()
        self._name = CouponName.DEAL_G20

    def is_applicable(self, orders, sub_total):
        return self.is_active() and sub_total >= COUPON_DEAL_G20_THRESHOLD_COST

    def discount_amount(self, orders, sub_total):
        return COUPON_DEAL_G20_DISCOUNT * sub_total if self.is_applicable(orders, sub_total) else 0


class DEAL_G5(Coupon):
    def __init__(self):
        super().__init__()
        self._name = CouponName.DEAL_G5

    def is_applicable(self, orders, sub_total):
        return self.is_active() and orders.total_quantity >= COUPON_DEAL_G5_THRESHOLD_QTY

    def discount_amount(self, orders, sub_total):
        return COUPON_DEAL_G5_DISCOUNT * sub_total if self.is_applicable(orders, sub_total) else 0


class CouponDiscount:
    def __init__(self, b4g1, deal_g20, deal_g5):
        self.b4g1 = b4g1
        self.deal_g20 = deal_g20
        self.deal_g5 = deal_g5

    def apply(self, orders, sub_total):
        applied_coupon = "NONE"
        coupon_discount = 0
        if self.b4g1.is_applicable(orders, sub_total):
            applied_coupon = self.b4g1.name
            coupon_discount = self.b4g1.discount_amount(orders, sub_total)
        else:
            d20 = self.deal_g20.discount_amount(orders, sub_total)
            d5 = self.deal_g5.discount_amount(orders, sub_total)
            if d20 > d5:
                applied_coupon = self.deal_g20.name
                coupon_discount = d20
            if d5 > d20:
                applied_coupon = self.deal_g5.name
                coupon_discount = d5
        return applied_coupon, coupon_discount

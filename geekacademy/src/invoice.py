from src.common.constants import *


class Invoice:
    def __init__(self, orders, coupon_discount):
        self._orders = orders
        self._coupon_discount = coupon_discount
        self._sub_total = 0
        self._membership_fee = 0
        self._total_membership_discount = 0
        self._enrollment_fee = 0
        self._total = 0
        self._total_coupon_discount = 0

    def compute(self):
        self._sub_total = self._orders.total_final_cost
        self._sub_total += self.membership_fee
        self._total_membership_discount = self._orders.total_membership_discount

        self._applied_coupon, self._total_coupon_discount = self._coupon_discount.apply(
            self._orders, self._sub_total)

    @property
    def total(self):
        return self._sub_total + self.enrollment_fee - self._total_coupon_discount

    @property
    def enrollment_fee(self):
        if self._sub_total < ENROLLMENT_THRESHOLD_COST:
            return ENROLLMENT_FEE
        else:
            return 0

    @property
    def membership_fee(self):
        return self._membership_fee

    @membership_fee.setter
    def membership_fee(self, fee):
        self._membership_fee = fee

    def get_bill(self) -> str:
        sub_total = f"SUB_TOTAL {self._sub_total:.2f}"
        coupon_discount = f"COUPON_DISCOUNT {self._applied_coupon} {self._total_coupon_discount:.2f}"
        pro_discount = f"TOTAL_PRO_DISCOUNT {self._total_membership_discount:.2f}"
        membership_fee = f"PRO_MEMBERSHIP_FEE {self.membership_fee:.2f}"
        enrollment_fee = f"ENROLLMENT_FEE {self.enrollment_fee:.2f}"
        total = f"TOTAL {self.total:.2f}"
        return "\n".join([sub_total, coupon_discount, pro_discount, membership_fee, enrollment_fee, total])

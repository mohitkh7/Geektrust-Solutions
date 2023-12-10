from src.common.constants import *


class MembershipDiscount:
    def __init__(self):
        self._discount = {}

    def add(self, programme, discount_percentage: int):
        self._discount[programme] = discount_percentage

    def get(self, programme) -> int:
        return self._discount.get(programme, 0)


class Membership:
    def __init__(self, membership_discount):
        self._is_pro_member = False
        self._membership_fee = 0
        self._membership_discount = membership_discount

    def add_pro_membership(self):
        self._is_pro_member = True    
        self._membership_fee = PRO_MEMBERSHIP_FEE

    def get_discount(self, programme) -> int:
        if self.is_pro_member:
            return self._membership_discount.get(programme)
        return 0

    @property
    def is_pro_member(self) -> bool:
        return self._is_pro_member

    @property
    def fee(self):
        return self._membership_fee



class Fee:
    def __init__(self, membership):
        self._fee_dict = {}
        self._membership = membership

    def add(self, programme, cost: int):
        self._fee_dict[programme] = cost

    def get(self, programme) -> (int, int):
        actual_cost = self.get_actual_cost(programme)
        discount = self.get_members_discount(programme) * actual_cost
        final_cost = actual_cost - discount
        return final_cost, discount

    def get_actual_cost(self, programme) -> int: 
        return self._fee_dict[programme]

    def get_members_discount(self, programme) -> int:
        return self._membership.get_discount(programme)

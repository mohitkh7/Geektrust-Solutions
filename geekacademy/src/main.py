from src.common.enums import Programme, Command, CouponName
from src.common.constants import *
from src.coupon import B4G1, DEAL_G20, DEAL_G5, CouponDiscount
from src.fee import MembershipDiscount, Membership, Fee
from src.invoice import Invoice
from src.order import OrderContainer


class GeekAcademy():
    def __init__(self):
        self.b4g1 = B4G1()
        self.deal_g20 = DEAL_G20()
        self.deal_g5 = DEAL_G5()
        self.coupon_discount = CouponDiscount(self.b4g1, self.deal_g20, self.deal_g5)

        membership_discount = MembershipDiscount()
        membership_discount.add(Programme.CERTIFICATION, CERTIFICATION_DISCOUNT)
        membership_discount.add(Programme.DEGREE, DEGREE_DISCOUNT)
        membership_discount.add(Programme.DIPLOMA, DIPLOMA_DISCOUNT)

        self.membership = Membership(membership_discount)

        self.fee = Fee(self.membership)    
        self.fee.add(Programme.CERTIFICATION, CERTIFICATION_FEE)
        self.fee.add(Programme.DEGREE, DEGREE_FEE)
        self.fee.add(Programme.DIPLOMA, DIPLOMA_FEE)

        self.orders = OrderContainer(self.fee)

        self.invoice = Invoice(self.orders, self.coupon_discount)

    def execute(self, instructions):
        for instruction in instructions:
            instruction = instruction.strip()
            args = instruction.split(" ")
            if args[0] == Command.ADD_PROGRAMME.value:
                self.add_programme(*args[1:])
            elif args[0] == Command.APPLY_COUPON.value:
                self.apply_coupon(*args[1:])
            elif args[0] == Command.ADD_PRO_MEMBERSHIP.value:
                self.add_pro_membership()
            elif args[0] == Command.PRINT_BILL.value:
                self.print_bill()
            else:
                raise ValueError(f"Unknown instruction found: {args[0]}")

    def add_programme(self, programme_type, quantity):
        for p in Programme:
            if programme_type == p.value:
                self.orders.add_programme(p, int(quantity))
                break
        else:
            raise ValueError(f"Unknown programme found: {programme_type}")

    def apply_coupon(self, coupon_name):
        if coupon_name == CouponName.DEAL_G20.value:
            self.deal_g20.activate()
        elif coupon_name == CouponName.DEAL_G5.value:
            self.deal_g5.activate()
        else:
            raise ValueError("Unknown coupon applied")

    def add_pro_membership(self):
        self.membership.add_pro_membership()
        self.invoice.membership_fee = PRO_MEMBERSHIP_FEE

    def print_bill(self):
        self.invoice.compute()
        print(self.invoice.get_bill())

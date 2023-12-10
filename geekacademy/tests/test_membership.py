import unittest
from unittest.mock import Mock

from src.fee import MembershipDiscount, Membership, Fee
from src.common.enums import Programme
from src.common.constants import PRO_MEMBERSHIP_FEE


class TestMembershipDiscount(unittest.TestCase):
	def setUp(self):
		self.obj = MembershipDiscount()

	def test_add_and_get_discount(self):
		self.obj.add(Programme.CERTIFICATION, 0.2)
		self.assertEqual(self.obj.get(Programme.CERTIFICATION), 0.2)

	def test_get_unknown_programme_discount(self):
		self.assertEqual(self.obj.get("UNKNOWN"), 0)


class TestMembership(unittest.TestCase):
	def setUp(self):
		self.membership_discount = Mock()
		self.membership_discount.get.return_value = 0.2
		self.membership = Membership(self.membership_discount)

	def test_add_pro_membership(self):
		self.membership.add_pro_membership()
		self.assertTrue(self.membership.is_pro_member)
		self.assertEqual(self.membership.fee, PRO_MEMBERSHIP_FEE)

	def test_get_discount_for_pro_member(self):
		self.membership.add_pro_membership()
		self.assertEqual(self.membership.get_discount(Programme.CERTIFICATION), 0.2)

	def test_get_discount_for_non_pro_member(self):
		self.assertEqual(self.membership.get_discount(Programme.CERTIFICATION), 0)


class TestFee(unittest.TestCase):
	def setUp(self):
		self.membership = Mock()
		self.fee = Fee(self.membership)

	def test_get_actual_cost(self):
		self.fee.add(Programme.CERTIFICATION, 3000)
		self.assertEqual(self.fee.get_actual_cost(Programme.CERTIFICATION), 3000)

	def test_get_members_discount(self):
		self.membership.get_discount.return_value = 0.2
		self.assertEqual(self.fee.get_members_discount(Programme.CERTIFICATION), 0.2)


	def test_get_fee(self):
		self.fee.add(Programme.CERTIFICATION, 1000)
		self.membership.get_discount.return_value = 0.2
		cost, discount = self.fee.get(Programme.CERTIFICATION)
		self.assertEqual(cost, 800)
		self.assertEqual(discount, 200)




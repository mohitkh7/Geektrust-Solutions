import unittest
from src.sip import SIP
from src.common.enums import Months


class TestSIP(unittest.TestCase):
    def test_sip_for_sip_month(self):
        sip = SIP(100)
        self.assertEqual(sip.get(Months.MAY), 100)

    def test_sip_for_non_sip_month(self):
        sip = SIP(100)
        self.assertEqual(sip.get(Months.JANUARY), 0)

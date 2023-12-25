import unittest
from src.asset import Asset
from src.history import History
from src.sip import SIP
from src.common.enums import Months
from unittest.mock import Mock


class TestAsset(unittest.TestCase):
    def test_set_and_get_amount(self):
        asset = Asset("SampleAsset", History())
        asset.set_amount(Months.MAY, 100)
        self.assertEqual(asset.get_amount(Months.MAY), 100)

    def test_apply_monthly_change(self):
        sip = Mock()
        sip.get.return_value = 20
        asset = Asset("SampleAsset", History())
        asset.set_sip(sip)
        asset.set_amount(Months.APRIL, 80)

        asset.apply_monthly_change(Months.MAY, '10%')

        self.assertEqual(asset.get_amount(Months.MAY), 110)

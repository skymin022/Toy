from django.test import TestCase
from .models import StockKRPrice

class StockKRPriceTest(TestCase):
    def test_create(self):
        obj = StockKRPrice.objects.create(
            code='005930', name='삼성전자', date='2025-06-16',
            open=80000, high=81000, low=79000, close=80500, volume=1000000)
        self.assertEqual(obj.close, 80500)

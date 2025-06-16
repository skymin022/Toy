# stock_global/models.py
from django.db import models

class StockGlobalPrice(models.Model):
    symbol = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    market = models.CharField(max_length=20)

    class Meta:
        unique_together = ('symbol', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.symbol} {self.date}"
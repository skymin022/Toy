# stock_kr/models.py
from django.db import models

class StockKRPrice(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('code', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.code} {self.name} {self.date}"
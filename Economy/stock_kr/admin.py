from django.contrib import admin
from .models import StockKRPrice

@admin.register(StockKRPrice)
class StockKRPriceAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'date', 'close', 'volume')
    search_fields = ('code', 'name')
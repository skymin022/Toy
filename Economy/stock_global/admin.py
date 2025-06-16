from django.contrib import admin
from .models import StockGlobalPrice

@admin.register(StockGlobalPrice)
class StockGlobalPriceAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'market', 'date', 'close', 'volume')
    search_fields = ('symbol', 'name', 'market')
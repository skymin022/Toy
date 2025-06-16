from django.shortcuts import render, get_object_or_404
from .models import StockGlobalPrice

def stock_global_chart(request, symbol):
    qs = StockGlobalPrice.objects.filter(symbol=symbol).order_by('date')
    if not qs.exists():
        return render(request, 'stock_global/not_found.html', {'symbol': symbol})
    data = {
        'labels': [str(obj.date) for obj in qs],
        'close': [obj.close for obj in qs],
    }
    return render(request, 'stock_global/chart.html', {'data': data, 'symbol': symbol})
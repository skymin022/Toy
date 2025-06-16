from django.shortcuts import render
from stock_kr.models import StockKRPrice
from stock_global.models import StockGlobalPrice

def compare_stocks(request, kr_code, global_symbol):
    kr_qs = StockKRPrice.objects.filter(code=kr_code).order_by('date')
    global_qs = StockGlobalPrice.objects.filter(symbol=global_symbol).order_by('date')
    if not kr_qs.exists() or not global_qs.exists():
        return render(request, 'dashboard/not_found.html', {'kr_code': kr_code, 'global_symbol': global_symbol})
    data = {
        'kr': {
            'labels': [str(obj.date) for obj in kr_qs],
            'close': [obj.close for obj in kr_qs],
        },
        'global': {
            'labels': [str(obj.date) for obj in global_qs],
            'close': [obj.close for obj in global_qs],
        }
    }
    return render(request, 'dashboard/compare.html', {'data': data, 'kr_code': kr_code, 'global_symbol': global_symbol})
from django.shortcuts import render, redirect
from .models import StockKRPrice

def search_stock(request):
    if request.method == 'GET' and 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
        start = request.GET.get('start')
        end = request.GET.get('end')
        # 종목명으로 코드 검색 (DB에 저장된 데이터에서)
        qs = StockKRPrice.objects.filter(name__icontains=keyword).order_by('-date')
        if qs.exists():
            code = qs.first().code
            # 차트 페이지로 이동 (GET 파라미터로 기간 전달)
            return redirect(f'/kr/chart/{code}/?start={start}&end={end}')
        else:
            return render(request, 'stock_kr/not_found.html', {'keyword': keyword})
    return render(request, 'stock_kr/search.html')


def stock_kr_chart(request, code):
    start = request.GET.get('start')
    end = request.GET.get('end')
    qs = StockKRPrice.objects.filter(code=code)
    if start:
        qs = qs.filter(date__gte=start)
    if end:
        qs = qs.filter(date__lte=end)
    qs = qs.order_by('date')
    data = {
        'labels': [str(obj.date) for obj in qs],
        'close': [obj.close for obj in qs],
    }
    return render(request, 'stock_kr/chart.html', {'data': data, 'code': code})


from django.shortcuts import render
from .models import StockKRPrice
from django.db.models import Max, Q

def stock_kr_list(request):
    # 종목코드별로 가장 최근 데이터만 한 건씩 출력
    latest_dates = (
        StockKRPrice.objects.values('code')
        .annotate(latest_date=Max('date'))
    )
    # code, latest_date 쌍으로 필터링
    filters = [
        {'code': item['code'], 'date': item['latest_date']}
        for item in latest_dates
    ]
    # 해당 code, date 쌍에 해당하는 객체만 가져오기
    query = Q()
    for f in filters:
        query |= (Q(code=f['code']) & Q(date=f['date']))
    stocks = StockKRPrice.objects.filter(query).order_by('name')
    return render(request, 'stock_kr/list.html', {'stocks': stocks})

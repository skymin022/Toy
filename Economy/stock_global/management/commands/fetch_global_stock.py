from django.core.management.base import BaseCommand
from stock_global.models import StockGlobalPrice
import yfinance as yf

class Command(BaseCommand):
    help = '해외 주식 데이터를 수집하여 저장합니다.'

    def add_arguments(self, parser):
        parser.add_argument('symbol', type=str, help='종목 심볼')
        parser.add_argument('name', type=str, help='종목명')
        parser.add_argument('market', type=str, help='시장명')
        parser.add_argument('--start', type=str, default='2018-01-01')
        parser.add_argument('--end', type=str, default=None)

    def handle(self, *args, **kwargs):
        symbol = kwargs['symbol']
        name = kwargs['name']
        market = kwargs['market']
        start = kwargs['start']
        end = kwargs['end']
        df = yf.download(symbol, start=start, end=end)
        for date, row in df.iterrows():
            StockGlobalPrice.objects.update_or_create(
                symbol=symbol, date=date,
                defaults={
                    'name': name,
                    'open': row['Open'],
                    'high': row['High'],
                    'low': row['Low'],
                    'close': row['Close'],
                    'volume': row['Volume'],
                    'market': market,
                }
            )
        self.stdout.write(self.style.SUCCESS(f"{symbol} 데이터 저장 완료"))

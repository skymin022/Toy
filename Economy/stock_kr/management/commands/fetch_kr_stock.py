from django.core.management.base import BaseCommand
from stock_kr.models import StockKRPrice
import FinanceDataReader as fdr

class Command(BaseCommand):
    help = '국내 주식 데이터를 수집하여 저장합니다.'

    def add_arguments(self, parser):
        parser.add_argument('code', type=str, help='KRX 종목코드')
        parser.add_argument('name', type=str, help='종목명')
        parser.add_argument('--start', type=str, default='2018-01-01')
        parser.add_argument('--end', type=str, default=None)

    def handle(self, *args, **kwargs):
        code = kwargs['code']
        name = kwargs['name']
        start = kwargs['start']
        end = kwargs['end']
        try:
            df = fdr.DataReader(code, start, end)
            for date, row in df.iterrows():
                StockKRPrice.objects.update_or_create(
                    code=code, date=date,
                    defaults={
                        'name': name,
                        'open': row['Open'],
                        'high': row['High'],
                        'low': row['Low'],
                        'close': row['Close'],
                        'volume': row['Volume'],
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"{code} 데이터 저장 완료"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"에러 발생: {e}"))

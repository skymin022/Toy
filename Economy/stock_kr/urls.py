from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_stock, name='stock_kr_chart'),
    path('list/', views.stock_kr_list, name='stock_kr_list'),
    path('chart/<str:code>/', views.stock_kr_chart, name='stock_kr_chart'),
    # ... (차트 뷰 등 추가)
]

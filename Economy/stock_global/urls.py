from django.urls import path
from . import views

urlpatterns = [
    path('chart/<str:symbol>/', views.stock_global_chart, name='stock_global_chart'),
]
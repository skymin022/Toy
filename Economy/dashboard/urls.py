from django.urls import path
from . import views

urlpatterns = [
    path('compare/<str:kr_code>/<str:global_symbol>/', views.compare_stocks, name='compare_stocks'),
]
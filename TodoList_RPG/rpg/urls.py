from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.stat_view, name='stat_view'),
    path('achievements/', views.achievement_list, name='achievement_list'),
]

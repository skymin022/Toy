from django.urls import path
from . import views

urlpatterns = [
    path('stats/', views.stat_view, name='stat_view'),
    path('achievements/', views.achievement_list, name='achievement_list'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('get-children-categories/', views.get_children_categories, name='get_children_categories'),
]

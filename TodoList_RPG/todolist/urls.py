from django.urls import path
from . import views
from .views import main_view

urlpatterns = [
    path('', views.todo_list, name='todo_list'),
    path('create/', views.todo_create, name='todo_create'),
    path('complete/<int:pk>/', views.todo_complete, name='todo_complete'),
    path('delete/<int:pk>/', views.todo_delete, name='todo_delete'),
]
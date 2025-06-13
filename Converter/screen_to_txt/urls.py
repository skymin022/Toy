from django.urls import path
from . import views

urlpatterns = [
    path('', views.screen_to_txt_view, name='screen_to_txt'),
]

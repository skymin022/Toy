from django.urls import path
from . import views

app_name = 'screen_to_txt'

urlpatterns = [
    path('', views.screen_to_txt_view, name='index'),
]

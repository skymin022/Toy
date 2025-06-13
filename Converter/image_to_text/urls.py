from django.urls import path
from . import views

app_name = 'image_to_text'

urlpatterns = [
    path('', views.image_to_text_view, name='index'),
]

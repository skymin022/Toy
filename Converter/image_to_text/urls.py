from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_to_text_view, name='image_to_text'),
]

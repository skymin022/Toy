from django.urls import path
from . import views

urlpatterns = [
    path('', views.pdf_to_txt_view, name='pdf_to_txt'),
]

from django.urls import path
from . import views

app_name = 'pdf_to_txt'


urlpatterns = [
    path('', views.pdf_to_txt_view, name='index'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='upload'),
    path('select/', views.select_files, name='select_files'),
    path('save/', views.save_txt, name='save_txt'),
]

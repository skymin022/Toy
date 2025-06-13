from django.urls import path
from . import views

app_name = 'folder_to_txt'


urlpatterns = [
    path('', views.index, name='index'),
    path('select/', views.select_files, name='select_files'),
    path('save/', views.save_txt, name='save_txt'),
]

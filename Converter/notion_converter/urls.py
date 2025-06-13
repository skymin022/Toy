from django.urls import path
from . import views

app_name = 'notion_converter'

urlpatterns = [
    path('', views.notion_upload, name='index'),    # 메인 업로드 및 변환 폼
    path('tistory/', views.tistory_upload, name='tistory_upload'),  # Tistory 업로드 폼 및 결과
]

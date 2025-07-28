from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),              # 최상위 경로: HTML 폼 페이지
    path('generate/', views.generate_code_view, name='generate_code'),  # 코드 생성 POST 처리
]

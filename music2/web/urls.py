from django.urls import path
from . import views

urlpatterns = [
    path('board/', views.board_list, name='board_list'),
    path('board/post/<int:pk>/', views.post_detail, name='post_detail'),  # 상세 페이지 별도 구현 필요
    path('board/post/create/', views.PostCreateView.as_view(), name='post_create'),

    # 관리자 승인 관련
    path('admin/posts/pending/', views.pending_posts, name='admin_pending_posts'),
    path('admin/posts/<int:post_id>/approve/', views.approve_post, name='approve_post'),
    path('admin/posts/<int:post_id>/reject/', views.reject_post, name='reject_post'),
]

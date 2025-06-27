from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    STATUS_CHOICES = (
        ('pending', '승인대기'),
        ('approved', '승인됨'),
        ('rejected', '반려됨'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    # 기타 필드(예: 게시판, 이미지 등)

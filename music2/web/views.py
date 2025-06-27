from django.shortcuts import render

# Create your views here.
from django.views.generic.edit import CreateView
from .models import Post

class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content']  # 기타 필드 추가 가능

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.status = 'pending'  # 승인 대기 상태로 저장
        return super().form_valid(form)


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

@staff_member_required
def approve_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.status = 'approved'
    post.save()
    # 알림 발송 등 추가
    return redirect(reverse('admin_pending_posts'))

@staff_member_required
def reject_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.status = 'rejected'
    post.save()
    # 알림 발송 등 추가
    return redirect(reverse('admin_pending_posts'))


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import Post

@staff_member_required
def pending_posts(request):
    posts = Post.objects.filter(status='pending')
    return render(request, 'admin/pending_posts.html', {'posts': posts})

# 게시판 목록 뷰
def board_list(request):
    posts = Post.objects.filter(status='approved').order_by('-created_at')
    return render(request, 'board/list.html', {'posts': posts})

# 예시: Django signals 활용
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Post)
def notify_user_on_approval(sender, instance, created, **kwargs):
    if not created and instance.status in ['approved', 'rejected']:
        # 실시간 알림/이메일 발송 로직
        pass

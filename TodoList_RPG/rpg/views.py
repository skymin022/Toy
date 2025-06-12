from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .forms import CategoryForm
from .models import Achievement, Category, Stat, UserCategoryStat
from django.contrib.auth.decorators import login_required
from django.db import models
from django.http import JsonResponse



@login_required
def category_list(request):
    # 대분류만 보여줌
    categories = Category.objects.filter(level=1)
    return render(request, 'rpg/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        level = request.POST.get('level')
        large_id = request.POST.get('large-category')
        middle_id = request.POST.get('middle-category')
        small_id = request.POST.get('small-category')

        # 가장 하위(소→중→대) 선택값을 parent로 사용
        parent_id = small_id or middle_id or large_id
        parent = Category.objects.get(id=parent_id) if parent_id else None

        # level 자동 판별(생략 가능, 폼에서 받는다면)
        if not level:
            if small_id:
                level = 3
            elif middle_id:
                level = 2
            else:
                level = 1

        # 중복 체크: 동일한 name, parent, level이 이미 존재하면 추가 안 함
        exists = Category.objects.filter(name=name, parent=parent, level=level).exists()
        if exists:
            messages.error(request, "이미 동일한 카테고리가 존재합니다.")
        elif name and level:
            Category.objects.create(name=name, level=level, parent=parent)
            messages.success(request, "카테고리가 추가되었습니다.")
            return redirect('category_list')

    large_categories = Category.objects.filter(level=1)
    middle_categories = Category.objects.filter(level=2)
    small_categories = Category.objects.filter(level=3)
    return render(request, 'rpg/category_form.html', {
        'large_categories': large_categories,
        'middle_categories': middle_categories,
        'small_categories': small_categories,
    })




@login_required
def stat_view(request):
    # 대분류만 보여줌
    categories = Category.objects.filter(level=1)
    user_stats = []
    for cat in categories:
        # 해당 대분류의 소분류 점수 합산
        sub_cats = Category.objects.filter(parent=cat)
        value = UserCategoryStat.objects.filter(user=request.user, category__in=sub_cats).aggregate(models.Sum('value'))['value__sum'] or 0
        user_stats.append({'category': cat.name, 'value': value})
    stat, _ = Stat.objects.get_or_create(user=request.user)
    return render(request, 'rpg/stat_view.html', {'stat': stat, 'user_stats': user_stats})


@login_required
def achievement_list(request):
    achievements = Achievement.objects.filter(user=request.user)
    return render(request, 'rpg/achievement_list.html', {'achievements': achievements})


def get_children_categories(request):
    parent_id = request.GET.get('parent_id')
    level = int(request.GET.get('level', 2))
    if parent_id:
        categories = Category.objects.filter(parent_id=parent_id, level=level)
    else:
        categories = Category.objects.none()
    data = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return JsonResponse({'categories': data})

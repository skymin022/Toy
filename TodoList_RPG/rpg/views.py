from django.shortcuts import render, redirect
from .forms import CategoryForm
from .models import Achievement, Category, Stat, UserCategoryStat
from django.contrib.auth.decorators import login_required
from django.db import models


@login_required
def category_list(request):
    # 대분류만 보여줌
    categories = Category.objects.filter(level=1)
    return render(request, 'rpg/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    large_categories = Category.objects.filter(level=1)
    return render(request, 'rpg/category_form.html', {'form': form, 'large_categories': large_categories})




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

from django.http import JsonResponse

def get_children_categories(request):
    parent_id = request.GET.get('parent_id')
    level = int(request.GET.get('level', 2))
    if parent_id:
        categories = Category.objects.filter(parent_id=parent_id, level=level)
    else:
        categories = Category.objects.filter(parent=None, level=1)
    data = [{'id': cat.id, 'name': cat.name} for cat in categories]
    return JsonResponse({'categories': data})

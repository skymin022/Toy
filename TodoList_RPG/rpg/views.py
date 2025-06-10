from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Stat, Achievement

@login_required
def stat_view(request):
    stat, _ = Stat.objects.get_or_create(user=request.user)
    return render(request, 'rpg/stat_view.html', {'stat': stat})

@login_required
def achievement_list(request):
    achievements = Achievement.objects.filter(user=request.user)
    return render(request, 'rpg/achievement_list.html', {'achievements': achievements})

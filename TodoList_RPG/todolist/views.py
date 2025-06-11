from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from django.contrib.auth.decorators import login_required
from .forms import TodoForm

@login_required
def todo_list(request):
    todos = Todo.objects.filter(user=request.user).order_by('-created')
    return render(request, 'todolist/todo_list.html', {'todos': todos})

@login_required
def todo_create(request):
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect('todo_list')
    else:
        form = TodoForm()
    return render(request, 'todolist/todo_form.html', {'form': form})

@login_required
def todo_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.completed = True
    todo.save()
    return redirect('todo_list')

@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.delete()
    return redirect('todo_list')

@login_required
def main_view(request):
    return render(request, 'main.html')
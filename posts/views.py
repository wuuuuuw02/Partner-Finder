from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Request
from .forms import RequestForm


@login_required
def create_request_view(request):
    """Страница создания заявки"""
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.author = request.user
            request_obj.save()
            messages.success(request, 'Запрос успешно создан!')
            return redirect('posts:requests_feed')
    else:
        form = RequestForm()
    
    return render(request, 'posts/create_request.html', {'form': form})


@login_required
def requests_feed_view(request):
    """Лента всех запросов"""
    requests_list = Request.objects.filter(is_active=True).select_related('author')
    
    request_type = request.GET.get('type')
    if request_type:
        requests_list = requests_list.filter(request_type=request_type)
    
    search_query = request.GET.get('search')
    if search_query:
        requests_list = requests_list.filter(
            models.Q(title__icontains=search_query) | 
            models.Q(description__icontains=search_query)
        )
    
    context = {
        'requests': requests_list,
        'request_type': request_type,
        'search_query': search_query,
    }
    return render(request, 'posts/requests_feed.html', context)


@login_required
def request_detail_view(request, pk):
    """Детальный просмотр заявки"""
    req = get_object_or_404(Request, pk=pk, is_active=True)
    return render(request, 'posts/request_detail.html', {'req': req})


@login_required
def edit_request_view(request, pk):
    """Редактирование заявки"""
    req = get_object_or_404(Request, pk=pk, author=request.user, is_active=True)
    
    if request.method == 'POST':
        form = RequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Заявка успешно обновлена!')
            return redirect('posts:request_detail', pk=req.pk)
    else:
        form = RequestForm(instance=req)
    
    return render(request, 'posts/edit_request.html', {'form': form, 'req': req})


@login_required
def delete_request_view(request, pk):
    """Удаление заявки"""
    req = get_object_or_404(Request, pk=pk, author=request.user, is_active=True)
    
    if request.method == 'POST':
        req.delete()
        messages.success(request, 'Заявка удалена.')
        return redirect('posts:requests_feed')
    
    return render(request, 'posts/confirm_delete.html', {'req': req})
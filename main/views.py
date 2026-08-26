# main/views.py

from django.shortcuts import render
from posts.models import Request

def home_view(request):
    """Главная страница"""
    if request.user.is_authenticated:
        user_requests = Request.objects.filter(
            author=request.user, 
            is_active=True
        ).order_by('-created_at')[:5]
        return render(request, 'main/home.html', {'user_requests': user_requests})
    else:
        return render(request, 'main/landing.html')
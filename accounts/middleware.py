# accounts/middleware.py

from django.utils import timezone
from django.contrib.auth.models import User

class ActiveUserMiddleware:
    """
    Middleware для отслеживания последней активности пользователя.
    Обновляет last_login при каждом запросе (если пользователь авторизован).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Обновляем last_login только если прошло больше 5 минут
            # (чтобы не писать в БД при каждом запросе)
            from datetime import timedelta
            if request.user.last_login is None or (timezone.now() - request.user.last_login) > timedelta(minutes=5):
                User.objects.filter(pk=request.user.pk).update(last_login=timezone.now())
        
        response = self.get_response(request)
        return response
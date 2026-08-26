# chats/models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Chat(models.Model):
    """
    Модель чата (диалога).
    В нашем случае чат всегда один на один, 
    поэтому мы ограничим участников логикой в будущем.
    """
    participants = models.ManyToManyField(
        User, 
        related_name='chats', 
        verbose_name='Участники'
    )
    hidden_by = models.ManyToManyField(User, related_name='hidden_chats', blank=True, verbose_name='Скрыт у')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Последняя активность')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-updated_at'] # Сначала показываем самые свежие чаты

    def __str__(self):
        # Показываем имена участников, чтобы было удобно в админке
        names = ", ".join([user.username for user in self.participants.all()])
        return f"Чат: {names}"

    def get_absolute_url(self):
        # Ссылка на этот чат (понадобится позже)
        return reverse('chat_detail', kwargs={'pk': self.pk})


class Message(models.Model):
    """
    Модель конкретного сообщения внутри чата.
    """
    chat = models.ForeignKey(
        Chat, 
        related_name='messages', 
        on_delete=models.CASCADE, 
        verbose_name='Чат'
    )
    sender = models.ForeignKey(
        User, 
        related_name='sent_messages', 
        on_delete=models.CASCADE, 
        verbose_name='Отправитель'
    )
    content = models.TextField(verbose_name='Текст сообщения')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время отправки')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['timestamp'] # Сообщения идут по времени (от старых к новым)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}..."
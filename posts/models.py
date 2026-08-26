from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Request(models.Model):
    """Модель заявки на поиск напарника"""
    
    REQUEST_TYPE_CHOICES = [
        ('games', '🎮 Games'),
        ('study', '📚 Study'),
        ('project', '💻 Project'),
        ('other', '🔧 Other'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests', verbose_name='Автор')
    title = models.CharField('Заголовок', max_length=200, help_text='Краткое описание вашей цели')
    description = models.TextField('Описание', help_text='Подробно опишите что вы ищете')
    request_type = models.CharField('Тип заявки', max_length=20, choices=REQUEST_TYPE_CHOICES, default='games')
    
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    is_active = models.BooleanField('Активна', default=True, help_text='Снимите галочку чтобы скрыть заявку')
    
    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.get_request_type_display()} - {self.title} ({self.author.username})'
    
    def get_type_icon(self):
        icons = {'games': '🎮', 'study': '📚', 'project': '💻', 'other': '🔧'}
        return icons.get(self.request_type, '📌')
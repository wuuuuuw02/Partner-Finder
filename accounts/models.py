import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import timedelta
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-created_at']

    def __str__(self):
        return f'Профиль {self.user.username}'
    
    @property
    def is_online(self):
        """Проверяет, онлайн ли пользователь (активность в последние 5 минут)"""
        if self.user.last_login is None:
            return False
        return (timezone.now() - self.user.last_login) < timedelta(minutes=5)
    
    def save(self, *args, **kwargs):
        """Переопределяем save для удаления старого аватара при обновлении"""
        if self.pk:  # Если профиль уже существует (не первое создание)
            try:
                old_profile = Profile.objects.get(pk=self.pk)
                if old_profile.avatar and old_profile.avatar != self.avatar:
                    # Старый аватар существует и он изменился - удаляем файл
                    if os.path.isfile(old_profile.avatar.path):
                        os.remove(old_profile.avatar.path)
            except Profile.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)

@receiver(post_delete, sender=Profile)
def delete_avatar_on_profile_delete(sender, instance, **kwargs):
    """Удаляем файл аватара при удалении профиля"""
    if instance.avatar:
        if os.path.isfile(instance.avatar.path):
            os.remove(instance.avatar.path)

class Comment(models.Model):
    """Комментарий/отзыв о пользователе"""
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments_made',
        verbose_name='Автор комментария'
    )
    target = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments_received',
        verbose_name='Пользователь'
    )
    content = models.TextField('Текст комментария', max_length=500)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
        unique_together = ['author', 'target']  # Один комментарий от одного пользователя
    
    def __str__(self):
        return f'{self.author.username} → {self.target.username}'


# ===== Сигналы (на уровне модуля, вне классов!) =====

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создаёт профиль при создании нового пользователя"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль при сохранении пользователя"""
    instance.profile.save()
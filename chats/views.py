from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Chat, Message
from django.db.models import Prefetch
from django.http import JsonResponse
from django.views.decorators.http import require_POST


@login_required
def chats_view(request):
    """Страница списка чатов"""
    user_chats = Chat.objects.filter(participants=request.user).exclude(hidden_by=request.user).prefetch_related(
        Prefetch('participants', queryset=User.objects.select_related('profile')),
        'messages'
    ).order_by('-updated_at')
    
    return render(request, 'chats/chats.html', {'chats': user_chats})


@login_required
def chat_detail_view(request, pk):
    """Страница конкретного чата"""
    chat = get_object_or_404(Chat, pk=pk, participants=request.user)
    
    user_chats = Chat.objects.filter(participants=request.user).exclude(hidden_by=request.user).prefetch_related(
        Prefetch('participants', queryset=User.objects.select_related('profile')),
        'messages'
    ).order_by('-updated_at')

    message_list = Message.objects.filter(chat=chat).select_related('sender')

    return render(request, 'chats/chat_detail.html', {
        'chat': chat,
        'user_chats': user_chats,
        'messages': message_list,
    })


@login_required
@require_POST
def delete_chat_view(request, pk):
    """Скрытие чата для текущего пользователя"""
    chat = get_object_or_404(Chat, pk=pk, participants=request.user)
    
    # Добавляем пользователя в список "скрыл чат"
    chat.hidden_by.add(request.user)
    messages.success(request, "Чат удален из списка.")
    
    return redirect('chats')


@login_required
def start_chat_view(request, user_id):
    """Создать новый чат с пользователем или перейти в существующий"""
    if user_id == request.user.id:
        messages.error(request, "Нельзя начать чат с самим собой.")
        return redirect('home')
    
    other_user = get_object_or_404(User, id=user_id)
    
    existing_chat = Chat.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()
    
    if existing_chat:
        existing_chat.hidden_by.remove(request.user)
        return redirect('chat_detail', pk=existing_chat.pk)
    else:
        new_chat = Chat.objects.create()
        new_chat.participants.add(request.user, other_user)
        # ✅ Добавляем заметное сообщение
        messages.success(
            request, 
            f'💬 Чат с {other_user.username} создан! Не забудьте оставить комментарий о пользователе на его профиле после общения.',
            extra_tags='chat_created'
        )
        return redirect('chat_detail', pk=new_chat.pk)

@login_required
@require_POST
def send_message_ajax(request, pk):
    """Отправка сообщения через AJAX (без перезагрузки страницы)"""
    chat = get_object_or_404(Chat, pk=pk, participants=request.user)
    
    content = request.POST.get('content', '').strip()
    
    if not content:
        return JsonResponse({'status': 'error', 'message': 'Сообщение пустое'}, status=400)
    
    # Создаём сообщение
    message = Message.objects.create(
        chat=chat,
        sender=request.user,
        content=content
    )
    
    # Обновляем время чата (чтобы он поднялся в списке)
    chat.save()
    chat.hidden_by.clear()
    
    # Возвращаем данные нового сообщения в формате JSON
    return JsonResponse({
        'status': 'success',
        'message': {
            'id': message.id,
            'content': message.content,
            'sender': message.sender.username,
            'sender_id': message.sender.id,
            'timestamp': message.timestamp.strftime('%H:%M'),
            'is_own': message.sender == request.user,
        }
    })

@login_required
def get_messages_ajax(request, pk):
    """Получение новых сообщений через AJAX (для polling)"""
    chat = get_object_or_404(Chat, pk=pk, participants=request.user)
    
    # Получаем ID последнего сообщения, которое уже есть у клиента
    last_id = request.GET.get('last_id', 0)
    
    # ✅ Проверяем, что last_id - это число
    try:
        last_id = int(last_id)
    except (ValueError, TypeError):
        last_id = 0
    
    # Ищем все сообщения в этом чате, которые новее last_id
    new_messages = Message.objects.filter(
        chat=chat, 
        id__gt=last_id
    ).select_related('sender').order_by('timestamp')
    
    messages_data = []
    for msg in new_messages:
        messages_data.append({
            'id': msg.id,
            'content': msg.content,
            'sender': msg.sender.username,
            'sender_id': msg.sender.id,
            'timestamp': msg.timestamp.strftime('%H:%M'),
            'is_own': msg.sender == request.user,
        })
        
    return JsonResponse({'messages': messages_data})
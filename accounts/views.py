from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserLoginForm, ProfileUpdateForm, CommentForm
from .models import User, Comment

def register_view(request):
    """Страница регистрации"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            messages.success(request, f"Добро пожаловать, {username}! Аккаунт успешно создан.")
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Страница входа"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
            
        messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Выход из аккаунта"""
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('home')

@login_required
def profile_view(request, pk=None):
    """Страница профиля (своего или чужого)"""
    if pk is None:
        # Если pk не передан — показываем свой профиль
        target_user = request.user
    else:
        # Иначе — профиль другого пользователя
        target_user = get_object_or_404(User, pk=pk)
    
    # Получаем комментарии к этому пользователю
    comments = target_user.comments_received.select_related('author').all()
    
    # Проверяем, есть ли комментарий от текущего пользователя
    user_comment = None
    if request.user != target_user:
        user_comment = comments.filter(author=request.user).first()
    
    context = {
        'target_user': target_user,
        'comments': comments,
        'user_comment': user_comment,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    """Страница редактирования профиля"""
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def add_comment_view(request, user_id):
    """Добавление комментария к пользователю"""
    target_user = get_object_or_404(User, id=user_id)
    
    # Нельзя оставить комментарий самому себе
    if target_user == request.user:
        messages.error(request, "Нельзя оставить комментарий самому себе.")
        return redirect('profile')
    
    # Проверяем, есть ли уже комментарий от этого пользователя
    existing_comment = Comment.objects.filter(author=request.user, target=target_user).first()
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if existing_comment:
                # Обновляем существующий комментарий
                existing_comment.content = form.cleaned_data['content']
                existing_comment.save()
                messages.success(request, 'Комментарий обновлён.')
            else:
                # Создаём новый комментарий
                Comment.objects.create(
                    author=request.user,
                    target=target_user,
                    content=form.cleaned_data['content']
                )
                messages.success(request, 'Комментарий добавлен.')
            return redirect('profile', pk=user_id)
    else:
        initial_content = existing_comment.content if existing_comment else ''
        form = CommentForm(initial={'content': initial_content})
    
    return render(request, 'accounts/add_comment.html', {
        'form': form,
        'target_user': target_user,
        'existing_comment': existing_comment,
    })

@login_required
def delete_comment_view(request, comment_id):
    """Удаление комментария"""
    comment = get_object_or_404(Comment, id=comment_id)
    target_user = comment.target
    
    # ✅ Проверяем права: автор комментария ИЛИ владелец профиля
    if request.user != comment.author and request.user != target_user:
        messages.error(request, "У вас нет прав на удаление этого комментария.")
        return redirect('profile', pk=target_user.id)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Комментарий удалён.')
    
    return redirect('profile', pk=target_user.id)
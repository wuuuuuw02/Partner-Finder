# PARTNER FINDER 🎯

**Partner Finder** — веб-приложение на Django для поиска напарников для совместных игр, учёбы и проектов. Платформа позволяет создавать заявки, просматривать ленту других участников, фильтровать по категориям, общаться в чатах, оставлять отзывы и находить единомышленников.

---

## 📋 Содержание

- [О проекте](#о-проекте)
- [Стек технологий](#стек-технологий)
- [Функционал](#функционал)
- [Структура проекта](#структура-проекта)
- [Установка и запуск](#установка-и-запуск)
- [Переменные окружения](#переменные-окружения)
- [Маршруты (URLs)](#маршруты-urls)
- [Модели данных](#модели-данных)
- [API эндпоинты (AJAX)](#api-эндпоинты-ajax)
- [Дизайн](#дизайн)
- [Планы по развитию](#планы-по-развитию)
- [Лицензия](#лицензия)

---

## 🚀 О проекте

**Partner Finder** решает проблему поиска единомышленников в трёх ключевых направлениях:

- **🎮 Games** — поиск напарников для совместных игровых сессий (CS2, Dota 2, Valorant и др.)
- **📚 Study** — поиск партнёров для совместной учёбы, подготовки к экзаменам
- **💻 Project** — поиск команды для IT-проектов, стартапов, хакатонов
- **🔧 Other** — всё остальное (спорт, творчество, путешествия)

Пользователи создают заявки с описанием того, кого они ищут, указывают цели, требования и предпочтения. Другие участники могут просматривать ленту заявок, фильтровать по типу, искать по ключевым словам, начинать диалог через встроенный чат и оставлять отзывы о пользователях.

---

## 🛠 Стек технологий

| Технология | Назначение |
|---|---|
| **Python 3.12+** | Язык программирования |
| **Django 6.0.2** | Веб-фреймворк |
| **PostgreSQL** | База данных |
| **python-decouple** | Управление переменными окружения |
| **HTML + CSS** | Интерфейс (киберпанк-стилистика) |
| **Google Fonts** | Шрифты Orbitron, Roboto Mono |
| **JavaScript (vanilla)** | AJAX-чаты (long-polling) |

---

## ✨ Функционал

### Реализовано ✅

#### 🔐 Аутентификация и пользователи
- **Регистрация** — создание нового аккаунта с уникальным email (валидация уникальности на уровне формы в [`UserRegisterForm`](accounts/forms.py:6))
- **Вход / Выход** — аутентификация пользователей через кастомные формы [`UserLoginForm`](accounts/forms.py:50)
- **Профиль пользователя** — просмотр профиля с аватаром, био, статусом онлайн, списком заявок и отзывами
- **Просмотр чужих профилей** — переход по `/accounts/profile/<id>/` с возможностью написать в чат и оставить отзыв
- **Редактирование профиля** — смена аватара и описания (bio) через [`ProfileUpdateForm`](accounts/forms.py:66)
- **Автоматическое создание профиля** — при регистрации пользователя через сигналы Django [`post_save`](accounts/models.py:60)
- **Отслеживание активности** — middleware [`ActiveUserMiddleware`](accounts/middleware.py:6) обновляет `last_login` каждые 5 минут, отображается статус «онлайн» в профиле

#### 📝 Заявки (Requests) — приложение [`posts`](posts/)
- **Создание заявки** — форма с выбором типа (Games / Study / Project / Other), заголовком и подробным описанием
- **Лента заявок** — просмотр всех активных заявок с пагинацией через `select_related` для оптимизации запросов
- **Фильтрация по типу** — быстрая фильтрация через выпадающий список (`?type=games`)
- **Поиск по тексту** — регистронезависимый поиск по заголовку и описанию (`?search=...`)
- **Детальный просмотр** — полная информация о заявке с возможностью написать автору
- **Редактирование заявки** — автор может изменить свою заявку (доступно только автору)
- **Удаление заявки** — автор может удалить свою заявку с подтверждением (страница подтверждения)

#### 💬 Чаты — приложение [`chats`](chats/)
- **Список чатов** — все активные диалоги пользователя, отсортированные по последней активности (`-updated_at`)
- **Личные сообщения** — обмен сообщениями с оптимизацией через `select_related('sender')`
- **Создание чата** — возможность начать диалог с другим пользователем (защита от создания чата с самим собой)
- **Поиск существующего чата** — если чат с пользователем уже существует, происходит переход в него (без дублирования)
- **AJAX-отправка сообщений** — отправка сообщений без перезагрузки страницы через [`send_message_ajax`](chats/views.py:92)
- **Long-polling обновление** — получение новых сообщений через [`get_messages_ajax`](chats/views.py:124) с передачей `last_id`
- **Отметка о прочтении** — поле `is_read` для отслеживания непрочитанных сообщений

#### ⭐ Система отзывов (Comments) — модель [`Comment`](accounts/models.py:31)
- **Добавление отзыва** — возможность оставить текстовый комментарий о другом пользователе
- **Редактирование отзыва** — при повторной отправке комментарий обновляется (один комментарий на пользователя)
- **Удаление отзыва** — автор или владелец профиля может удалить комментарий
- **Защита от само-комментирования** — нельзя оставить отзыв самому себе
- **Уникальность** — ограничение `unique_together = ['author', 'target']` гарантирует один отзыв от пользователя

#### 🎨 Интерфейс
- **Киберпанк-стилистика** — тёмная тема, неоново-зелёный акцент (`#00ff88`), моноширинные шрифты
- **Landing page** — приветственная страница для неавторизованных пользователей
- **Dashboard** — личный кабинет с быстрым доступом к созданию заявки и списком своих заявок (последние 5)
- **Адаптивный дизайн** — корректное отображение на мобильных устройствах
- **Система уведомлений** — flash-сообщения об успехе/ошибке через `django.contrib.messages`

### В планах 🔮

- [ ] Регистрация моделей в админ-панели (сейчас `admin.py` пусты)
- [ ] Возможность откликаться на заявки (система откликов)
- [ ] Улучшенная главная страница с лентой заявок вместо отдельной страницы
- [ ] Уведомления о новых сообщениях (email / in-app)
- [ ] Групповые чаты
- [ ] WebSockets для real-time чатов (вместо long-polling)
- [ ] CI/CD и деплой на продакшен

---

## 📁 Структура проекта

```
partner-finder/
├── core/                           # Конфигурация Django-проекта
│   ├── settings.py                 # Настройки проекта (PostgreSQL, static, media)
│   ├── urls.py                     # Корневой URL-конфиг (include всех приложений)
│   ├── wsgi.py                     # WSGI-точка входа
│   └── asgi.py                     # ASGI-точка входа
│
├── accounts/                       # Приложение пользователей
│   ├── models.py                   # Profile + Comment (отзывы), сигналы post_save
│   ├── views.py                    # Регистрация, логин, профиль, комментарии CRUD
│   ├── forms.py                    # UserRegisterForm, UserLoginForm, ProfileUpdateForm, CommentForm
│   ├── urls.py                     # Маршруты аккаунтов (8 маршрутов)
│   ├── middleware.py               # ActiveUserMiddleware — отслеживание активности
│   ├── admin.py                    # (пусто) — модели не зарегистрированы
│   └── templates/accounts/         # Шаблоны (base, login, register, profile, edit_profile)
│
├── posts/                          # Приложение заявок (requests)
│   ├── models.py                   # Request (заявка на поиск напарника)
│   ├── views.py                    # CRUD для заявок, лента, фильтрация, поиск
│   ├── forms.py                    # RequestForm (ModelForm)
│   ├── urls.py                     # Маршруты (namespace='posts', 5 маршрутов)
│   ├── admin.py                    # (пусто)
│   └── templates/posts/            # Шаблоны (create, edit, detail, feed, confirm_delete)
│
├── chats/                          # Приложение чатов
│   ├── models.py                   # Chat + Message
│   ├── views.py                    # Список чатов, детальный просмотр, отправка, AJAX
│   ├── forms.py                    # MessageForm
│   ├── urls.py                     # Маршруты чатов (6 маршрутов, включая AJAX)
│   ├── admin.py                    # (пусто)
│   └── templates/chats/            # Шаблоны (chats, chat_detail)
│
├── main/                           # Основное приложение (главная страница)
│   ├── views.py                    # home_view — dashboard / landing
│   ├── urls.py                     # Корневой маршрут '/'
│   └── templates/main/             # Шаблоны (home, landing)
│
├── static/                         # Статические файлы (CSS, JS)
├── media/                          # Медиа-файлы
│   └── avatars/                    # Загруженные аватары пользователей
│
├── .env                            # Переменные окружения (БД)
├── manage.py                       # Управляющий скрипт Django
└── README.md                       # Этот файл
```

---

## ⚙️ Установка и запуск

### Предварительные требования

- Python 3.12 или выше
- PostgreSQL
- pip (менеджер пакетов Python)

### Пошаговая инструкция

1. **Клонируйте репозиторий**

```bash
git clone https://github.com/your-username/partner-finder.git
cd partner-finder
```

2. **Создайте виртуальное окружение**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Установите зависимости**

```bash
pip install django python-decouple psycopg2-binary
```

4. **Настройте базу данных PostgreSQL**

Создайте базу данных в PostgreSQL:

```sql
CREATE DATABASE partner_finder;
```

5. **Настройте переменные окружения**

Создайте файл [`.env`](.env) в корне проекта:

```env
DB_NAME=partner_finder
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=django-insecure-your-secret-key-here
```

> **⚠️ Важно:** В текущей версии `SECRET_KEY` жёстко прописан в [`settings.py`](core/settings.py:25). Для продакшена обязательно вынесите его в `.env` через `config('SECRET_KEY')`.

6. **Выполните миграции**

```bash
python manage.py migrate
```

7. **Создайте суперпользователя (опционально)**

```bash
python manage.py createsuperuser
```

8. **Запустите сервер разработки**

```bash
python manage.py runserver
```

9. **Откройте в браузере**

```
http://127.0.0.1:8000/
```

---

## 🔐 Переменные окружения

Файл [`.env`](.env) содержит следующие переменные:

| Переменная | Описание | Значение по умолчанию |
|---|---|---|
| `DB_NAME` | Название базы данных | `partner_finder` |
| `DB_USER` | Пользователь БД | `postgres` |
| `DB_PASSWORD` | Пароль пользователя БД | — |
| `DB_HOST` | Хост БД | `localhost` |
| `DB_PORT` | Порт БД | `5432` |

> **Рекомендация:** Добавьте `SECRET_KEY` в `.env` и используйте `config('SECRET_KEY')` в [`settings.py`](core/settings.py) вместо хардкода.

---

## 🧭 Маршруты (URLs)

### Корневые маршруты ([`core/urls.py`](core/urls.py))

| Путь | Назначение |
|---|---|
| `/admin/` | Админ-панель Django |
| `/accounts/` | Маршруты приложения accounts |
| `/posts/` | Маршруты приложения posts (заявки) |
| `/chats/` | Маршруты приложения chats |
| `/` | Маршруты приложения main (главная) |

### Маршруты аккаунтов ([`accounts/urls.py`](accounts/urls.py))

| URL | Имя | View | Описание |
|---|---|---|---|
| `/accounts/register/` | `register` | `register_view` | Регистрация |
| `/accounts/login/` | `login` | `login_view` | Вход |
| `/accounts/logout/` | `logout` | `logout_view` | Выход |
| `/accounts/profile/` | `profile` | `profile_view` | Свой профиль |
| `/accounts/profile/<int:pk>/` | `profile` | `profile_view` | Профиль пользователя |
| `/accounts/profile/edit/` | `edit_profile` | `edit_profile_view` | Редактирование профиля |
| `/accounts/profile/<int:user_id>/comment/` | `add_comment` | `add_comment_view` | Добавление/редактирование отзыва |
| `/accounts/comment/<int:comment_id>/delete/` | `delete_comment` | `delete_comment_view` | Удаление отзыва |

### Маршруты заявок ([`posts/urls.py`](posts/urls.py)) — namespace: `posts`

| URL | Имя | View | Описание |
|---|---|---|---|
| `/posts/create/` | `posts:create_request` | `create_request_view` | Создание заявки |
| `/posts/` | `posts:requests_feed` | `requests_feed_view` | Лента заявок (с фильтрацией и поиском) |
| `/posts/<int:pk>/` | `posts:request_detail` | `request_detail_view` | Детальный просмотр |
| `/posts/<int:pk>/edit/` | `posts:edit_request` | `edit_request_view` | Редактирование заявки |
| `/posts/<int:pk>/delete/` | `posts:delete_request` | `delete_request_view` | Удаление заявки |

### Маршруты чатов ([`chats/urls.py`](chats/urls.py))

| URL | Имя | View | Описание |
|---|---|---|---|
| `/chats/` | `chats` | `chats_view` | Список чатов |
| `/chats/<int:pk>/` | `chat_detail` | `chat_detail_view` | Детальный просмотр чата |
| `/chats/<int:pk>/send/` | `send_message` | `send_message_view` | Отправка сообщения (POST-форма) |
| `/chats/<int:pk>/send-ajax/` | `send_message_ajax` | `send_message_ajax` | Отправка сообщения через AJAX |
| `/chats/<int:pk>/get-messages/` | `get_messages_ajax` | `get_messages_ajax` | Получение новых сообщений (long-polling) |
| `/chats/start/<int:user_id>/` | `start_chat` | `start_chat_view` | Создание нового чата |

### Маршруты главной ([`main/urls.py`](main/urls.py))

| URL | Имя | View | Описание |
|---|---|---|---|
| `/` | `home` | `home_view` | Dashboard (авторизован) / Landing (гость) |

---

## 💾 Модели данных

### Profile ([`accounts/models.py`](accounts/models.py:9))

Модель профиля пользователя, связанная один-к-одному со встроенной моделью `User`.

| Поле | Тип | Описание |
|---|---|---|
| `user` | `OneToOneField(User)` | Связь с пользователем |
| `bio` | `TextField(max_length=500)` | Описание / «О себе» |
| `avatar` | `ImageField(upload_to='avatars/')` | Аватар пользователя |
| `created_at` | `DateTimeField(auto_now_add=True)` | Дата регистрации |

**Методы:**
- [`is_online`](accounts/models.py:23) — `@property`, проверяет, был ли пользователь активен в последние 5 минут (на основе `last_login`)

Профиль создаётся автоматически при регистрации пользователя через сигнал [`post_save`](accounts/models.py:60).

### Comment ([`accounts/models.py`](accounts/models.py:31))

Модель отзыва/комментария о пользователе.

| Поле | Тип | Описание |
|---|---|---|
| `author` | `ForeignKey(User, related_name='comments_made')` | Автор комментария |
| `target` | `ForeignKey(User, related_name='comments_received')` | Пользователь, о котором отзыв |
| `content` | `TextField(max_length=500)` | Текст комментария |
| `created_at` | `DateTimeField(auto_now_add=True)` | Дата создания |

**Ограничения:**
- `unique_together = ['author', 'target']` — один пользователь может оставить только один отзыв о другом пользователе (при повторной отправке отзыв обновляется)

### Request ([`posts/models.py`](posts/models.py:7))

Модель заявки на поиск напарника.

| Поле | Тип | Описание |
|---|---|---|
| `author` | `ForeignKey(User, related_name='requests')` | Автор заявки |
| `title` | `CharField(max_length=200)` | Заголовок |
| `description` | `TextField` | Подробное описание |
| `request_type` | `CharField(max_length=20)` | Тип: `games`, `study`, `project`, `other` |
| `created_at` | `DateTimeField(default=timezone.now)` | Дата создания |
| `updated_at` | `DateTimeField(auto_now=True)` | Дата обновления (автоматически) |
| `is_active` | `BooleanField(default=True)` | Активна ли заявка |

**Методы:**
- [`get_type_icon()`](posts/models.py:34) — возвращает эмодзи-иконку для типа заявки

### Chat ([`chats/models.py`](chats/models.py:7))

Модель чата (диалога) между пользователями.

| Поле | Тип | Описание |
|---|---|---|
| `participants` | `ManyToManyField(User)` | Участники чата |
| `created_at` | `DateTimeField(auto_now_add=True)` | Дата создания |
| `updated_at` | `DateTimeField(auto_now=True)` | Последняя активность (автообновление) |

**Методы:**
- [`get_absolute_url()`](chats/models.py:31) — возвращает ссылку на детальный просмотр чата

### Message ([`chats/models.py`](chats/models.py:36))

Модель сообщения внутри чата.

| Поле | Тип | Описание |
|---|---|---|
| `chat` | `ForeignKey(Chat, related_name='messages')` | Чат, к которому относится сообщение |
| `sender` | `ForeignKey(User, related_name='sent_messages')` | Отправитель |
| `content` | `TextField` | Текст сообщения |
| `timestamp` | `DateTimeField(auto_now_add=True)` | Время отправки |
| `is_read` | `BooleanField(default=False)` | Прочитано ли сообщение |

---

## 🌐 API эндпоинты (AJAX)

Приложение [`chats`](chats/) предоставляет AJAX-эндпоинты для работы чата в реальном времени без перезагрузки страницы:

### Отправка сообщения
```
POST /chats/<int:pk>/send-ajax/
```
**Параметры:** `content` (текст сообщения)

**Ответ:**
```json
{
  "status": "success",
  "message": {
    "id": 1,
    "content": "Привет!",
    "sender": "username",
    "sender_id": 1,
    "timestamp": "14:30",
    "is_own": true
  }
}
```

### Получение новых сообщений (long-polling)
```
GET /chats/<int:pk>/get-messages/?last_id=0
```
**Параметры:** `last_id` — ID последнего полученного сообщения (0 — получить все)

**Ответ:**
```json
{
  "messages": [
    {
      "id": 1,
      "content": "Привет!",
      "sender": "username",
      "sender_id": 1,
      "timestamp": "14:30",
      "is_own": false
    }
  ]
}
```

---

## 🎨 Дизайн

Интерфейс выполнен в **киберпанк-стилистике**:

- **Цветовая схема**: тёмный фон (`#050505`), неоново-зелёный акцент (`#00ff88`)
- **Шрифты**: Orbitron (заголовки), Roboto Mono (основной текст)
- **Элементы**: карточки с тонкими границами, кнопки в стиле терминала, анимированные переходы
- **Атмосфера**: системные сообщения (`>>> SYSTEM ALERT`), технологичный UI
- **Навигация**: хедер с активными ссылками (Dashboard, Requests, Chats, Profile, Logout)

---

## 📄 Лицензия

Проект создан в образовательных целях. Все права защищены.

---

<div align="center">
  <sub>Built with Django 6.0.2 • 2026</sub>
</div>

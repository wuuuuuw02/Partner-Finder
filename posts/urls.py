# posts/urls.py

from django.urls import path
from . import views

app_name = 'posts'  # ✅ Важно! Это namespace для маршрутов

urlpatterns = [
    path('create/', views.create_request_view, name='create_request'),
    path('', views.requests_feed_view, name='requests_feed'),
    path('<int:pk>/', views.request_detail_view, name='request_detail'),
    path('<int:pk>/edit/', views.edit_request_view, name='edit_request'),
    path('<int:pk>/delete/', views.delete_request_view, name='delete_request'),
]
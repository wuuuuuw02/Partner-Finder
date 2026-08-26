from django.urls import path
from . import views

urlpatterns = [
    path('', views.chats_view, name='chats'),
    path('<int:pk>/', views.chat_detail_view, name='chat_detail'),
    path('<int:pk>/delete/', views.delete_chat_view, name='delete_chat'), 
    path('<int:pk>/send-ajax/', views.send_message_ajax, name='send_message_ajax'),
    path('<int:pk>/get-messages/', views.get_messages_ajax, name='get_messages_ajax'),
    path('start/<int:user_id>/', views.start_chat_view, name='start_chat'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:pk>/', views.profile_view, name='profile'), 
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('profile/<int:user_id>/comment/', views.add_comment_view, name='add_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment_view, name='delete_comment'), 
]
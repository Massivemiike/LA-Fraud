from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import UserLoginForm

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        authentication_form=UserLoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('verify-email/<int:user_id>/', views.verify_email, name='verify_email'),
    path('character-creation/<int:user_id>/', views.character_creation, name='character_creation'),
    path('profile/', views.profile_view, name='profile'),
]
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import RegisterView, UserProfileView, UserProfileUpdateView

#app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/post/<int:post_id>/', UserProfileView.as_view(), name='user-profile-from-post'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='profile-edit'),
]
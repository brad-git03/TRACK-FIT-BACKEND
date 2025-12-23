from django.urls import path
from .views import RegisterView, LoginView, UserProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # Add this path:
    path('profile/<int:user_id>/update/', UserProfileUpdateView.as_view(), name='update-profile'),    
]
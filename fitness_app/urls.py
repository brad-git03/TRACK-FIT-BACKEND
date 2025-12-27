from django.urls import path
from .views import StartWorkoutView, LogChallengeProgressView

urlpatterns = [
    # Existing endpoint for dashboard quick workouts
    path('workout/start/', StartWorkoutView.as_view(), name='start-workout'),
    
    # --- NEW ENDPOINT FOR CHALLENGE LOGGING ---
    path('challenge/<int:challenge_id>/log/', LogChallengeProgressView.as_view(), name='log-challenge-progress'),
]
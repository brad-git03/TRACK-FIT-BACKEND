from django.urls import path
from .views import StartWorkoutView

urlpatterns = [
    path('workout/start/', StartWorkoutView.as_view(), name='start-workout'),
]
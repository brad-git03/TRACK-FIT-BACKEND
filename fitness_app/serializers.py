# fitness_app/serializers.py
from rest_framework import serializers
from .models import WorkoutSession

class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = '__all__'
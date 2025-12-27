# fitness_app/serializers.py
from rest_framework import serializers
from .models import WorkoutSession, Challenge, ChallengeParticipant, ChallengeLog
from registration.serializers import UserSerializer

# --- 1. WORKOUT SESSION ---
class WorkoutSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutSession
        fields = '__all__'

# --- 2. CHALLENGE LOGS ---
class ChallengeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeLog
        fields = ['id', 'date', 'image', 'caption']

# --- 3. PARTICIPANTS (Fix is here) ---
class ChallengeParticipantSerializer(serializers.ModelSerializer):
    # This sends full details (avatar, name) for display
    user_details = UserSerializer(source='user', read_only=True)
    
    # CHANGE: Use email to identify the user uniquely in logic checks
    # This replaces "John Doe" with "john@example.com"
    user = serializers.SlugRelatedField(read_only=True, slug_field='email')

    class Meta:
        model = ChallengeParticipant
        fields = [
            'id', 'user', 'user_details', 
            'total_workouts', 'current_week_progress', 'streak', 
            'last_log_date', 'last_proof_image', 'last_caption'
        ]

# --- 4. CHALLENGES ---
class ChallengeSerializer(serializers.ModelSerializer):
    participants_data = ChallengeParticipantSerializer(source='participants', many=True, read_only=True)
    participants_count = serializers.IntegerField(source='participants.count', read_only=True)

    class Meta:
        model = Challenge
        fields = [
            'id', 'name', 'description', 'activity_type', 
            'start_date', 'end_date', 'host', 'status',
            'participants_count', 'participants_data',
            'group_goal_total', 'group_workouts_completed'
        ]
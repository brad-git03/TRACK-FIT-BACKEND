from rest_framework import serializers
from .models import UserRegistration

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        fields = '__all__'

# --- THIS WAS MISSING ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        # Add 'current_weight', 'height', 'unit_preference' to this list
        fields = [
            'id', 'first_name', 'last_name', 'email', 'role', 
            'profile_picture', 'bio', 'phone_number', 'address',
            'current_weight', 'height', 'unit_preference' # <--- NEW
        ]
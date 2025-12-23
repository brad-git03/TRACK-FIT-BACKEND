from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import UserRegistration
from .serializers import RegistrationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated

class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            # 1. Securely hash the password before saving
            password = serializer.validated_data['password']
            serializer.validated_data['password'] = make_password(password)
            
            # 2. Save the new user
            new_user = serializer.save()
            
            # 3. Return the safe user data (without password)
            return Response({
                "message": "User registered successfully",
                "user": UserSerializer(new_user).data
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # 1. Check if both fields are provided
        if not email or not password:
            return Response({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Try to find the user by email
        try:
            user = UserRegistration.objects.get(email=email)
        except UserRegistration.DoesNotExist:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        # 3. Check if the password matches the hash
        if check_password(password, user.password):
            # Login successful! Return the user data
            return Response({
                "message": "Login successful",
                "user": UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileUpdateView(APIView):
    # Depending on how you handle auth, you might need permission_classes = [IsAuthenticated]
    
    def patch(self, request, user_id):
        try:
            user = UserRegistration.objects.get(id=user_id)
        except UserRegistration.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
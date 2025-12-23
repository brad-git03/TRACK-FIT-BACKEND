# fitness_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkoutSessionSerializer
from registration.models import UserRegistration

class StartWorkoutView(APIView):
    def post(self, request):
        # We expect data like: {"user_id": 1, "activity_type": "Running", "source": "app"}
        user_id = request.data.get('user_id')
        
        try:
            user = UserRegistration.objects.get(id=user_id)
        except UserRegistration.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

        data = request.data.copy()
        data['user'] = user.id # Ensure the foreign key is set correctly
        
        serializer = WorkoutSessionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Workout Started!", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# fitness_app/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import WorkoutSessionSerializer
from registration.models import UserRegistration
from django.utils import timezone
from .models import Challenge, ChallengeParticipant, ChallengeLog
from .serializers import ChallengeSerializer # You need to create this

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

class LogChallengeProgressView(APIView):
    def post(self, request, challenge_id):
        user = request.user # Requires IsAuthenticated permission
        
        # 1. Get the participant record
        try:
            participant = ChallengeParticipant.objects.get(
                challenge_id=challenge_id, 
                user__email=request.data.get('email') # Or use request.user if using Token Auth
            )
        except ChallengeParticipant.DoesNotExist:
            return Response({'error': 'Not a participant'}, status=404)

        # 2. Check if already logged today
        today = timezone.now().date()
        if participant.last_log_date == today:
             return Response({'error': 'Already logged today'}, status=400)

        # 3. Create the Log
        image = request.FILES.get('image')
        caption = request.data.get('caption')
        
        log = ChallengeLog.objects.create(
            participant=participant,
            image=image,
            caption=caption
        )

        # 4. Update Participant Stats
        participant.total_workouts += 1
        participant.current_week_progress += 1
        
        # Simple Streak Logic
        if participant.last_log_date == (today - timezone.timedelta(days=1)):
            participant.streak += 1
        elif participant.last_log_date != today:
            participant.streak = 1 # Reset if skipped a day (unless today is the log)
            
        participant.last_log_date = today
        participant.last_proof_image = image # Cache for easy display
        participant.last_caption = caption
        participant.save()

        return Response({'message': 'Progress logged!'}, status=200)
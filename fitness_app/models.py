from django.db import models
from registration.models import UserRegistration

# --- 1. EXISTING WORKOUT SESSION MODEL ---
class WorkoutSession(models.Model):
    ACTIVITY_CHOICES = [
        ('Walking', 'Walking'),
        ('Running', 'Running'),
        ('Biking', 'Biking'),
    ]
    
    SOURCE_CHOICES = [
        ('app', 'In-App Tracker'),
        ('3rd_party', '3rd Party Connector'),
    ]

    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    start_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return f"{self.user.first_name} - {self.activity_type} ({self.start_time})"

# --- 2. NEW CHALLENGE MODELS (The missing parts) ---

class Challenge(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    activity_type = models.CharField(max_length=50, default='Workout') # e.g., 'Running', 'Walking'
    
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    host = models.CharField(max_length=150) # Stores username of the creator
    status = models.CharField(max_length=20, default='Active')
    
    # Group Progress Tracking
    group_goal_total = models.IntegerField(default=100)
    group_workouts_completed = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class ChallengeParticipant(models.Model):
    challenge = models.ForeignKey(Challenge, related_name='participants', on_delete=models.CASCADE)
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    
    # Individual Stats
    total_workouts = models.IntegerField(default=0)
    current_week_progress = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    last_log_date = models.DateField(null=True, blank=True)
    
    # Caching last upload for easy display in feeds
    last_proof_image = models.ImageField(upload_to='proofs/', null=True, blank=True)
    last_caption = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} in {self.challenge.name}"

class ChallengeLog(models.Model):
    participant = models.ForeignKey(ChallengeParticipant, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='proofs/', null=True, blank=True)
    caption = models.TextField(blank=True, null=True)
    
    class Meta:
        # Prevent double logging on the same day for the same person
        unique_together = ('participant', 'date')
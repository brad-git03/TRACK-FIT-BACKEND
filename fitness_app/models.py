# fitness_app/models.py
from django.db import models
from registration.models import UserRegistration # Import your user model

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
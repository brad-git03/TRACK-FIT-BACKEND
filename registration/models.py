from django.db import models

class UserRegistration(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('User', 'User'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='User')

    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    
    # Optional fields
    bio = models.TextField(blank=True, null=True, help_text="About User")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    current_weight = models.FloatField(null=True, blank=True, help_text="Weight in KG")
    height = models.FloatField(null=True, blank=True, help_text="Height in CM")
    unit_preference = models.CharField(max_length=10, default='metric', choices=[('metric', 'Metric'), ('imperial', 'Imperial')])

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
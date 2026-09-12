from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone as django_timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    timezone = models.CharField(max_length=63, default='UTC')
    
    # Preferences
    theme = models.CharField(max_length=20, default='dark', choices=[('dark', 'Dark Theme'), ('light', 'Light Theme'), ('system', 'System Default')])
    email_notifications = models.BooleanField(default=True)
    reduced_motion = models.BooleanField(default=False)
    profile_visibility = models.CharField(max_length=20, default='public', choices=[('public', 'Public'), ('friends', 'Friends Only'), ('private', 'Private')])
    
    last_active_at = models.DateTimeField(default=django_timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Required for custom user
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

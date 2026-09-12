from django.db import models
from django.conf import settings

class NotificationType(models.TextChoices):
    QUEST_COMPLETED = 'QUEST_COMPLETED', 'Quest Completed'
    LEVEL_UP = 'LEVEL_UP', 'Level Up'
    ACHIEVEMENT_UNLOCKED = 'ACHIEVEMENT_UNLOCKED', 'Achievement Unlocked'
    ITEM_PURCHASED = 'ITEM_PURCHASED', 'Item Purchased'
    STREAK_MILESTONE = 'STREAK_MILESTONE', 'Streak Milestone'
    SYSTEM = 'SYSTEM', 'System'

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NotificationType.choices, default=NotificationType.SYSTEM)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

from django.db import models
from django.conf import settings
import uuid

class WebhookToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='webhook_tokens')
    name = models.CharField(max_length=100)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class IntegrationRule(models.Model):
    token = models.ForeignKey(WebhookToken, on_delete=models.CASCADE, related_name='rules')
    source_event = models.CharField(max_length=100, help_text="e.g. github.push, fitbit.step_goal")
    target_quest = models.ForeignKey('quests.Quest', on_delete=models.CASCADE, null=True, blank=True)
    target_habit = models.ForeignKey('quests.Habit', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Rule: {self.source_event} -> Quest {self.target_quest_id} / Habit {self.target_habit_id}"

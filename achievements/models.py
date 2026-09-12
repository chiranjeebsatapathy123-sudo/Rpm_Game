from django.db import models
from django.conf import settings

class Achievement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='🏆') # Emoji or CSS class
    
    # Milestone criteria
    criteria_type = models.CharField(max_length=50, choices=[
        ('LEVEL', 'Reach Level'),
        ('QUESTS_COMPLETED', 'Quests Completed'),
        ('STREAK', 'Habit Streak'),
        ('BOSS_KILLS', 'Boss Kills')
    ], default='LEVEL')
    criteria_value = models.IntegerField(default=1)
    
    # Rewards
    reward_xp = models.IntegerField(default=0)
    reward_gold = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class UserAchievement(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    unlocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'achievement')

    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"

from django.db import models
from django.conf import settings
from social.models import Party

class Boss(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    max_health = models.IntegerField(default=10000)
    difficulty = models.CharField(max_length=50, default='HARD')
    reward_xp_pool = models.IntegerField(default=5000)
    reward_gold_pool = models.IntegerField(default=2000)
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='bosses/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.max_health} HP)"

class PartyBattle(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='battles')
    boss = models.ForeignKey(Boss, on_delete=models.CASCADE, related_name='battles')
    current_health = models.IntegerField()
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_victorious = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.current_health = self.boss.max_health
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.party.name} vs {self.boss.name}"

class DamageLog(models.Model):
    battle = models.ForeignKey(PartyBattle, on_delete=models.CASCADE, related_name='damage_logs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    damage_dealt = models.IntegerField()
    quest = models.ForeignKey('quests.Quest', on_delete=models.SET_NULL, null=True, blank=True)
    habit = models.ForeignKey('quests.Habit', on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} dealt {self.damage_dealt} to {self.battle.boss.name}"

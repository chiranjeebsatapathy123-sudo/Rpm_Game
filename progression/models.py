from django.db import models
from django.conf import settings

class XPTransactionType(models.TextChoices):
    QUEST = 'QUEST', 'Quest'
    ACHIEVEMENT = 'ACHIEVEMENT', 'Achievement'
    BONUS = 'BONUS', 'Bonus'
    ADMIN = 'ADMIN', 'Admin'

class XPTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='xp_transactions')
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=50, choices=XPTransactionType.choices, default=XPTransactionType.QUEST)
    quest = models.ForeignKey('quests.Quest', on_delete=models.SET_NULL, null=True, blank=True, related_name='xp_transactions')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.amount} XP | {self.transaction_type}"

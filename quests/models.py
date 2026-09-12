from django.db import models
from django.conf import settings

class QuestStatus(models.TextChoices):
    TODO = 'TODO', 'To Do'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'
    ARCHIVED = 'ARCHIVED', 'Archived'

class QuestCategory(models.TextChoices):
    STUDY = 'STUDY', 'Study'
    CODING = 'CODING', 'Coding'
    FITNESS = 'FITNESS', 'Fitness'
    HEALTH = 'HEALTH', 'Health'
    READING = 'READING', 'Reading'
    WORK = 'WORK', 'Work'
    FINANCE = 'FINANCE', 'Finance'
    SOCIAL = 'SOCIAL', 'Social'
    PERSONAL = 'PERSONAL', 'Personal'
    MEDITATION = 'MEDITATION', 'Meditation'
    CUSTOM = 'CUSTOM', 'Custom'

class QuestAttribute(models.TextChoices):
    STRENGTH = 'STRENGTH', 'Strength'
    INTELLECT = 'INTELLECT', 'Intellect'
    AGILITY = 'AGILITY', 'Agility'
    VITALITY = 'VITALITY', 'Vitality'
    WISDOM = 'WISDOM', 'Wisdom'
    DISCIPLINE = 'DISCIPLINE', 'Discipline'
    CHARISMA = 'CHARISMA', 'Charisma'

class QuestDifficulty(models.TextChoices):
    EASY = 'EASY', 'Easy'
    MEDIUM = 'MEDIUM', 'Medium'
    HARD = 'HARD', 'Hard'
    EPIC = 'EPIC', 'Epic'

class Quest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quests')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=QuestCategory.choices, default=QuestCategory.CUSTOM)
    attribute = models.CharField(max_length=50, choices=QuestAttribute.choices, default=QuestAttribute.STRENGTH)
    difficulty = models.CharField(max_length=50, choices=QuestDifficulty.choices, default=QuestDifficulty.MEDIUM)
    
    estimated_minutes = models.IntegerField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    recurring = models.BooleanField(default=False)
    recurrence_rule = models.CharField(max_length=255, blank=True, help_text="e.g., daily, weekly")
    
    status = models.CharField(max_length=50, choices=QuestStatus.choices, default=QuestStatus.TODO)
    
    xp_reward = models.IntegerField(default=50)
    gold_reward = models.IntegerField(default=25)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='habits')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=QuestCategory.choices, default=QuestCategory.CUSTOM)
    attribute = models.CharField(max_length=50, choices=QuestAttribute.choices, default=QuestAttribute.STRENGTH)
    difficulty = models.CharField(max_length=50, choices=QuestDifficulty.choices, default=QuestDifficulty.MEDIUM)
    
    xp_reward = models.IntegerField(default=20)
    gold_reward = models.IntegerField(default=10)
    
    streak_count = models.IntegerField(default=0)
    last_completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"

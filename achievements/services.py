from django.contrib.auth import get_user_model
from .models import Achievement, UserAchievement
from quests.models import Quest

def check_achievements(user, character=None):
    """
    Evaluates if the user has unlocked any new achievements.
    Returns a list of newly unlocked UserAchievement objects.
    """
    newly_unlocked = []
    
    # Get un-earned achievements
    earned_ids = UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True)
    available_achievements = Achievement.objects.exclude(id__in=earned_ids)
    
    if not available_achievements.exists():
        return newly_unlocked

    char = character or user.character
    quests_completed = Quest.objects.filter(user=user, status='COMPLETED').count()
    
    for ach in available_achievements:
        unlocked = False
        
        if ach.criteria_type == 'LEVEL' and char.level >= ach.criteria_value:
            unlocked = True
        elif ach.criteria_type == 'QUESTS_COMPLETED' and quests_completed >= ach.criteria_value:
            unlocked = True
        # Future expansions could add STREAK and BOSS_KILLS parsing here
        
        if unlocked:
            ua = UserAchievement.objects.create(user=user, achievement=ach)
            # Give rewards
            char.total_xp += ach.reward_xp
            char.gold += ach.reward_gold
            char.save()
            newly_unlocked.append(ua)
            
    return newly_unlocked

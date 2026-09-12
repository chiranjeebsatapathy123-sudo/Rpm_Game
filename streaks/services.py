from django.utils import timezone
from .models import Streak

def update_streak(user):
    """
    Updates the user's streak.
    If activity is on the next consecutive day: current_streak += 1
    If activity occurs on the same day: do not increment again.
    If a day was missed: reset current streak appropriately.
    """
    now = timezone.now()
    today = timezone.localtime(now).date()
    
    streak, created = Streak.objects.get_or_create(user=user)
    
    if streak.last_activity_date == today:
        # Same day, no change
        return streak
        
    if streak.last_activity_date:
        delta = today - streak.last_activity_date
        if delta.days == 1:
            streak.current_streak += 1
        else:
            streak.current_streak = 1
    else:
        streak.current_streak = 1

    if streak.current_streak > streak.longest_streak:
        streak.longest_streak = streak.current_streak

    streak.last_activity_date = today
    streak.save()
    
    return streak

from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Achievement, UserAchievement
from quests.models import Quest


User = get_user_model()


@transaction.atomic
def check_achievements(user, character=None):
    newly_unlocked = []

    earned_ids = UserAchievement.objects.filter(
        user=user
    ).values_list(
        'achievement_id',
        flat=True
    )

    available_achievements = Achievement.objects.exclude(
        id__in=earned_ids
    )

    if not available_achievements.exists():
        return newly_unlocked

    if character is None:
        character, _ = user.character.__class__.objects.get_or_create(
            user=user
        )

    quests_completed = Quest.objects.filter(
        user=user,
        status='COMPLETED'
    ).count()

    streak = getattr(user, 'streak', None)

    current_streak = 0

    if streak is not None:
        current_streak = streak.current_streak

    for achievement in available_achievements:
        unlocked = False

        if (
            achievement.criteria_type == 'LEVEL'
            and character.level >= achievement.criteria_value
        ):
            unlocked = True

        elif (
            achievement.criteria_type == 'QUESTS_COMPLETED'
            and quests_completed >= achievement.criteria_value
        ):
            unlocked = True

        elif (
            achievement.criteria_type == 'STREAK'
            and current_streak >= achievement.criteria_value
        ):
            unlocked = True

        elif achievement.criteria_type == 'BOSS_KILLS':
            boss_kills = 0

            if hasattr(user, 'boss_kills'):
                boss_kills = user.boss_kills

            if boss_kills >= achievement.criteria_value:
                unlocked = True

        if unlocked:
            user_achievement, created = UserAchievement.objects.get_or_create(
                user=user,
                achievement=achievement
            )

            if created:
                character.total_xp += achievement.reward_xp
                character.gold += achievement.reward_gold

                newly_unlocked.append(user_achievement)

    if newly_unlocked:
        from progression.services import calculate_level

        character.level = calculate_level(
            character.total_xp
        )

        character.save(
            update_fields=[
                'total_xp',
                'gold',
                'level'
            ]
        )

    return newly_unlocked
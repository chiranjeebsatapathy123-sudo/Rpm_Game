from django.utils import timezone
from django.db import transaction
from django.core.exceptions import PermissionDenied
from .models import QuestStatus

from character.models import Character
from progression.models import XPTransaction, XPTransactionType
from progression.services import calculate_level
from rewards.models import GoldTransaction, GoldTransactionType
from streaks.services import update_streak
from notifications.models import Notification, NotificationType
from battles.models import PartyBattle, DamageLog

@transaction.atomic
def complete_quest(user, quest):
    if quest.user != user:
        raise PermissionDenied("You do not own this quest.")
        
    if quest.status == QuestStatus.COMPLETED:
        raise ValueError("Quest is already completed.")

    # 1. Update Quest
    quest.status = QuestStatus.COMPLETED
    quest.completed_at = timezone.now()
    quest.save()

    # 2. Get Character
    character, _ = Character.objects.select_for_update().get_or_create(user=user)
    
    # 3. Calculate Rewards with Equipment Multipliers
    xp = int(quest.xp_reward * character.equipment_xp_multiplier)
    gold = int(quest.gold_reward * character.equipment_gold_multiplier)
    
    # 4. Apply Rewards to Character
    character.total_xp += xp
    character.gold += gold
    
    # Attribute XP (Simplified: +1 to attribute per completion, or could scale)
    attr_field = quest.attribute.lower()
    if hasattr(character, attr_field):
        current_attr_val = getattr(character, attr_field)
        setattr(character, attr_field, current_attr_val + 1)
        
    # 5. Create Ledgers
    XPTransaction.objects.create(
        user=user,
        amount=xp,
        transaction_type=XPTransactionType.QUEST,
        quest=quest,
        description=f"Completed quest: {quest.title}"
    )
    
    GoldTransaction.objects.create(
        user=user,
        amount=gold,
        transaction_type=GoldTransactionType.EARN,
        quest=quest,
        description=f"Completed quest: {quest.title}"
    )

    # 6. Check Level Up
    old_level = character.level
    new_level = calculate_level(character.total_xp)
    level_up = new_level > old_level
    
    if level_up:
        character.level = new_level
        Notification.objects.create(
            user=user,
            title="Level Up!",
            message=f"You reached Level {new_level}!",
            notification_type=NotificationType.LEVEL_UP
        )

    character.save()

    # 7. Update Streak
    streak = update_streak(user)

    # 8. Check Achievements (Moved to Celery Task)
    # 9. Create Notification
    Notification.objects.create(
        user=user,
        title="Quest Completed",
        message=f"You earned {xp} XP and {gold} Gold.",
        notification_type=NotificationType.QUEST_COMPLETED
    )
    
    # Boss Battle Hook
    boss_damage_dealt = 0
    active_battles = PartyBattle.objects.filter(party__members=user, is_victorious=False)
    for battle in active_battles:
        # Damage equals base XP of the quest
        damage = quest.xp_reward
        battle.current_health -= damage
        boss_damage_dealt += damage
        DamageLog.objects.create(battle=battle, user=user, damage_dealt=damage, quest=quest)
        
        if battle.current_health <= 0:
            battle.current_health = 0
            battle.is_victorious = True
            battle.completed_at = timezone.now()
            # Distribute boss rewards (simplified: give boss pool to everyone)
            for member in battle.party.members.all():
                char, _ = Character.objects.get_or_create(user=member)
                char.total_xp += battle.boss.reward_xp_pool
                char.gold += battle.boss.reward_gold_pool
                char.save()
                Notification.objects.create(
                    user=member, title="Boss Defeated!", 
                    message=f"Your party defeated {battle.boss.name}! +{battle.boss.reward_xp_pool} XP", 
                    notification_type="SYSTEM"
                )
        battle.save()
    
    if quest.recurring:
        # Simplified recurring logic: clone and set status to TODO, clear completed_at
        pass
        
    from achievements.tasks import process_achievements_task
    process_achievements_task.delay(user.id)

    return {
        "success": True,
        "xp_earned": xp,
        "gold_earned": gold,
        "attribute": quest.attribute,
        "attribute_xp": 1,
        "new_total_xp": character.total_xp,
        "new_level": character.level,
        "level_up": level_up,
        "streak": streak.current_streak,
        # We don't return newly unlocked achievements synchronously anymore to keep API fast
        "achievements": [] 
    }

@transaction.atomic
def complete_habit(user, habit):
    if habit.user != user:
        raise PermissionDenied("You do not own this habit.")
        
    now = timezone.now()
    if habit.last_completed_at and habit.last_completed_at.date() == now.date():
        raise ValueError("Habit is already completed for today.")

    # Calculate local streak
    if habit.last_completed_at and habit.last_completed_at.date() == (now.date() - timezone.timedelta(days=1)):
        habit.streak_count += 1
    else:
        habit.streak_count = 1
        
    habit.last_completed_at = now
    habit.save()

    character, _ = Character.objects.select_for_update().get_or_create(user=user)
    
    # Apply equipment multipliers
    xp = int(habit.xp_reward * character.equipment_xp_multiplier)
    gold = int(habit.gold_reward * character.equipment_gold_multiplier)
    
    character.total_xp += xp
    character.gold += gold
    
    attr_field = habit.attribute.lower()
    if hasattr(character, attr_field):
        current_attr_val = getattr(character, attr_field)
        setattr(character, attr_field, current_attr_val + 1)
        
    XPTransaction.objects.create(
        user=user,
        amount=xp,
        transaction_type=XPTransactionType.QUEST,
        description=f"Completed habit: {habit.title}"
    )
    
    GoldTransaction.objects.create(
        user=user,
        amount=gold,
        transaction_type=GoldTransactionType.EARN,
        description=f"Completed habit: {habit.title}"
    )

    old_level = character.level
    new_level = calculate_level(character.total_xp)
    level_up = new_level > old_level
    
    if level_up:
        character.level = new_level
        Notification.objects.create(
            user=user, title="Level Up!", message=f"You reached Level {new_level}!", notification_type=NotificationType.LEVEL_UP
        )

    character.save()
    streak = update_streak(user)
    
    Notification.objects.create(
        user=user, title="Habit Completed", message=f"You earned {xp} XP and {gold} Gold.", notification_type=NotificationType.QUEST_COMPLETED
    )
    
    # Boss Battle Hook
    boss_damage_dealt = 0
    active_battles = PartyBattle.objects.filter(party__members=user, is_victorious=False)
    for battle in active_battles:
        damage = habit.xp_reward
        battle.current_health -= damage
        boss_damage_dealt += damage
        DamageLog.objects.create(battle=battle, user=user, damage_dealt=damage, habit=habit)
        
        if battle.current_health <= 0:
            battle.current_health = 0
            battle.is_victorious = True
            battle.completed_at = timezone.now()
            for member in battle.party.members.all():
                char, _ = Character.objects.get_or_create(user=member)
                char.total_xp += battle.boss.reward_xp_pool
                char.gold += battle.boss.reward_gold_pool
                char.save()
                Notification.objects.create(
                    user=member, title="Boss Defeated!", 
                    message=f"Your party defeated {battle.boss.name}! +{battle.boss.reward_xp_pool} XP", 
                    notification_type="SYSTEM"
                )
        battle.save()

    from achievements.tasks import process_achievements_task
    process_achievements_task.delay(user.id)

    return {
        "success": True,
        "xp_earned": xp,
        "gold_earned": gold,
        "attribute": habit.attribute,
        "attribute_xp": 1,
        "new_total_xp": character.total_xp,
        "new_level": character.level,
        "level_up": level_up,
        "streak": streak.current_streak,
        "boss_damage_dealt": boss_damage_dealt,
        "achievements": []
    }

from django.core.management.base import BaseCommand
from accounts.models import User
from character.models import Character, RPGClass
from quests.models import Quest, QuestCategory, QuestAttribute, QuestDifficulty, QuestStatus
from progression.models import XPTransaction, XPTransactionType
from progression.services import calculate_level
from rewards.models import GoldTransaction, GoldTransactionType
from streaks.models import Streak

class Command(BaseCommand):
    help = 'Creates demo data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating Demo Data...")

        if User.objects.filter(email='demo@example.com').exists():
            self.stdout.write(self.style.WARNING("Demo user already exists."))
            return

        # Create Demo User
        user = User.objects.create_user(username='demo_hero', email='demo@example.com', password='password123')
        
        # Create Character
        char = Character.objects.create(
            user=user, 
            rpg_class=RPGClass.WARRIOR,
            level=3,
            total_xp=650,
            gold=420,
            strength=15,
            intellect=12,
            agility=10,
            vitality=18,
            wisdom=8,
            discipline=14,
            charisma=10
        )

        # Create Streak
        Streak.objects.create(
            user=user,
            current_streak=5,
            longest_streak=12,
            last_activity_date=None
        )

        # Create Quests
        quests = [
            {"title": "100 Pushups", "cat": QuestCategory.FITNESS, "attr": QuestAttribute.STRENGTH, "diff": QuestDifficulty.MEDIUM},
            {"title": "Read 20 pages", "cat": QuestCategory.READING, "attr": QuestAttribute.INTELLECT, "diff": QuestDifficulty.EASY},
            {"title": "Code for 2 hours", "cat": QuestCategory.CODING, "attr": QuestAttribute.INTELLECT, "diff": QuestDifficulty.HARD},
            {"title": "Meditate 10 mins", "cat": QuestCategory.MEDITATION, "attr": QuestAttribute.WISDOM, "diff": QuestDifficulty.EASY},
        ]

        for q in quests:
            Quest.objects.create(
                user=user,
                title=q['title'],
                category=q['cat'],
                attribute=q['attr'],
                difficulty=q['diff'],
                xp_reward=50,
                gold_reward=25
            )

        # Create some history
        XPTransaction.objects.create(user=user, amount=650, transaction_type=XPTransactionType.ADMIN, description="Initial grant")
        GoldTransaction.objects.create(user=user, amount=420, transaction_type=GoldTransactionType.BONUS, description="Initial grant")

        self.stdout.write(self.style.SUCCESS("Demo data created successfully. Login with demo_hero / password123"))

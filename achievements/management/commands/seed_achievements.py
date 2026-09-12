from django.core.management.base import BaseCommand
from achievements.models import Achievement

class Command(BaseCommand):
    help = 'Seeds initial achievements for the RPG'

    def handle(self, *args, **kwargs):
        achievements = [
            {
                "name": "Novice Adventurer",
                "description": "Reach Level 5",
                "icon": "🌟",
                "criteria_type": "LEVEL",
                "criteria_value": 5,
                "reward_xp": 500,
                "reward_gold": 100
            },
            {
                "name": "Journeyman",
                "description": "Reach Level 10",
                "icon": "🛡️",
                "criteria_type": "LEVEL",
                "criteria_value": 10,
                "reward_xp": 1000,
                "reward_gold": 250
            },
            {
                "name": "Quest Master",
                "description": "Complete 10 Quests",
                "icon": "📜",
                "criteria_type": "QUESTS_COMPLETED",
                "criteria_value": 10,
                "reward_xp": 800,
                "reward_gold": 200
            },
            {
                "name": "Overachiever",
                "description": "Complete 50 Quests",
                "icon": "👑",
                "criteria_type": "QUESTS_COMPLETED",
                "criteria_value": 50,
                "reward_xp": 3000,
                "reward_gold": 1000
            }
        ]

        for data in achievements:
            obj, created = Achievement.objects.get_or_create(
                name=data["name"],
                defaults=data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created achievement: {obj.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Achievement already exists: {obj.name}'))

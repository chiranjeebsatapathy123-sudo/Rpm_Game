from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rewards.models import ShopItem, ShopItemType
from battles.models import Boss

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds data for the LIFE RPG Expansion Pack features'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting expansion seed...")

        # 1. Create Equipment (Phase 2)
        equipment_data = [
            {
                "name": "Sword of Discipline",
                "description": "Boosts XP earned from quests by 10%. Adds +5 STR.",
                "item_type": ShopItemType.WEAPON,
                "price": 500,
                "rarity": "RARE",
                "metadata": {"bonus_str": 5, "bonus_xp_pct": 10}
            },
            {
                "name": "Amulet of Wealth",
                "description": "Boosts Gold earned by 20%. Adds +2 CHA.",
                "item_type": ShopItemType.ACCESSORY,
                "price": 1000,
                "rarity": "EPIC",
                "metadata": {"bonus_cha": 2, "bonus_gold_pct": 20}
            }
        ]

        for ed in equipment_data:
            item, created = ShopItem.objects.get_or_create(name=ed["name"], defaults=ed)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created equipment: {item.name}"))

        # 2. Create Boss (Phase 4)
        boss, created = Boss.objects.get_or_create(
            name="Procrastinator Dragon",
            defaults={
                "description": "A massive beast that drains your willpower and delays your quests.",
                "max_health": 500, # Lowered for testing
                "difficulty": "EPIC",
                "reward_xp_pool": 10000,
                "reward_gold_pool": 5000,
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created Boss: {boss.name}"))

        self.stdout.write(self.style.SUCCESS('Successfully seeded expansion data!'))

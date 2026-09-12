from django.core.management.base import BaseCommand
from achievements.models import Achievement
from rewards.models import ShopItem, ShopItemType

class Command(BaseCommand):
    help = 'Seeds initial game data like Achievements and Shop Items'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding Game Data...")

        # Achievements
        achievements = [
            {"name": "First Steps", "description": "Complete your first quest.", "req_type": "QUESTS_COMPLETED", "req_val": 1, "xp": 100, "gold": 50},
            {"name": "Apprentice", "description": "Complete 10 quests.", "req_type": "QUESTS_COMPLETED", "req_val": 10, "xp": 500, "gold": 250},
            {"name": "Dedicated", "description": "Reach a 7-day streak.", "req_type": "STREAK", "req_val": 7, "xp": 1000, "gold": 500},
            {"name": "Awakened", "description": "Reach Level 5.", "req_type": "LEVEL", "req_val": 5, "xp": 1500, "gold": 750},
        ]

        for a in achievements:
            obj, created = Achievement.objects.get_or_create(
                name=a['name'],
                defaults={
                    "description": a['description'],
                    "criteria_type": a['req_type'],
                    "criteria_value": a['req_val'],
                    "reward_xp": a['xp'],
                    "reward_gold": a['gold']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Achievement: {obj.name}"))

        # Extensive Shop Items
        shop_items = [
            # Titles
            {"name": "Title: The Relentless", "desc": "Equip this title to show your dedication.", "type": ShopItemType.TITLE, "price": 1000, "rarity": "RARE"},
            {"name": "Title: The Awakened", "desc": "You have realized your potential.", "type": ShopItemType.TITLE, "price": 5000, "rarity": "EPIC"},
            {"name": "Title: Conqueror", "desc": "The ultimate title.", "type": ShopItemType.TITLE, "price": 15000, "rarity": "LEGENDARY"},
            
            # Frames
            {"name": "Obsidian Frame", "desc": "A dark obsidian avatar frame.", "type": ShopItemType.FRAME, "price": 1500, "rarity": "EPIC"},
            {"name": "Golden Halo", "desc": "A glowing golden frame.", "type": ShopItemType.FRAME, "price": 3000, "rarity": "LEGENDARY"},
            {"name": "Wooden Frame", "desc": "A simple rustic frame.", "type": ShopItemType.FRAME, "price": 300, "rarity": "COMMON"},
            
            # Weapons
            {"name": "Novice Sword", "desc": "A standard iron sword.", "type": ShopItemType.WEAPON, "price": 100, "rarity": "COMMON"},
            {"name": "Steel Longsword", "desc": "A well-balanced weapon.", "type": ShopItemType.WEAPON, "price": 750, "rarity": "UNCOMMON"},
            {"name": "Dragonbane Halberd", "desc": "A mythical weapon.", "type": ShopItemType.WEAPON, "price": 10000, "rarity": "LEGENDARY"},
            {"name": "Crystal Staff", "desc": "Pulses with arcane energy.", "type": ShopItemType.WEAPON, "price": 4000, "rarity": "EPIC"},
            {"name": "Shadow Daggers", "desc": "Perfect for a rogue.", "type": ShopItemType.WEAPON, "price": 2500, "rarity": "RARE"},
            
            # Armor
            {"name": "Leather Tunic", "desc": "Basic protection.", "type": ShopItemType.ARMOR, "price": 150, "rarity": "COMMON"},
            {"name": "Chainmail", "desc": "Heavy but protective.", "type": ShopItemType.ARMOR, "price": 900, "rarity": "UNCOMMON"},
            {"name": "Mithril Plate", "desc": "Lightweight and indestructible.", "type": ShopItemType.ARMOR, "price": 12000, "rarity": "LEGENDARY"},
            {"name": "Archmage Robes", "desc": "Woven from starlight.", "type": ShopItemType.ARMOR, "price": 8000, "rarity": "EPIC"},
            
            # Effects
            {"name": "Crimson Aura", "desc": "A fiery red aura for your profile.", "type": ShopItemType.EFFECT, "price": 500, "rarity": "UNCOMMON"},
            {"name": "Elixir of Wisdom", "desc": "Boosts INT by 5 permanently.", "type": ShopItemType.EFFECT, "price": 2500, "rarity": "LEGENDARY"},
            {"name": "Shadow Step", "desc": "Leave a trail of darkness.", "type": ShopItemType.EFFECT, "price": 1200, "rarity": "RARE"},
        ]

        for i in shop_items:
            obj, created = ShopItem.objects.get_or_create(
                name=i['name'],
                defaults={
                    "description": i['desc'],
                    "item_type": i['type'],
                    "price": i['price'],
                    "rarity": i['rarity']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Shop Item: {obj.name}"))
        
        # Add some Raid Bosses
        from battles.models import Boss
        bosses = [
            {"name": "Gorgoroth The Destroyer", "desc": "A massive dragon terrorizing the kingdom.", "difficulty": "EPIC", "health": 150000},
            {"name": "Shadow Knight", "desc": "An ancient undead warrior.", "difficulty": "HARD", "health": 50000},
            {"name": "Slime King", "desc": "A giant gelatinous cube.", "difficulty": "MEDIUM", "health": 10000},
            {"name": "Bandit Leader", "desc": "A ruthless thug.", "difficulty": "EASY", "health": 2500},
            {"name": "The Void Walker", "desc": "An entity from beyond the stars.", "difficulty": "LEGENDARY", "health": 500000},
        ]
        
        for b in bosses:
            obj, created = Boss.objects.get_or_create(
                name=b['name'],
                defaults={
                    "description": b['desc'],
                    "difficulty": b['difficulty'],
                    "max_health": b['health'],
                    "active": True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Boss: {obj.name}"))

        self.stdout.write(self.style.SUCCESS("Seeding complete."))

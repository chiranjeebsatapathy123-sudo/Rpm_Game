from django.db import models
from django.conf import settings

class RPGClass(models.TextChoices):
    WARRIOR = 'WARRIOR', 'Warrior'
    MAGE = 'MAGE', 'Mage'
    ROGUE = 'ROGUE', 'Rogue'
    RANGER = 'RANGER', 'Ranger'
    MONK = 'MONK', 'Monk'
    ENGINEER = 'ENGINEER', 'Engineer'
    NONE = 'NONE', 'None'

class Character(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='character')
    rpg_class = models.CharField(max_length=20, choices=RPGClass.choices, default=RPGClass.NONE)
    
    # Core stats
    level = models.IntegerField(default=1)
    total_xp = models.BigIntegerField(default=0)
    gold = models.IntegerField(default=100)
    health = models.IntegerField(default=100)
    energy = models.IntegerField(default=100)
    
    # Attributes
    strength = models.IntegerField(default=10)
    intellect = models.IntegerField(default=10)
    agility = models.IntegerField(default=10)
    vitality = models.IntegerField(default=10)
    wisdom = models.IntegerField(default=10)
    discipline = models.IntegerField(default=10)
    charisma = models.IntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _get_equipment_bonus(self, stat_name):
        bonus = 0
        for inv in self.user.inventory.filter(equipped=True):
            if inv.item.metadata and isinstance(inv.item.metadata, dict):
                bonus += inv.item.metadata.get(f"bonus_{stat_name}", 0)
        return bonus

    @property
    def total_strength(self): return self.strength + self._get_equipment_bonus('str')
    @property
    def total_intellect(self): return self.intellect + self._get_equipment_bonus('int')
    @property
    def total_agility(self): return self.agility + self._get_equipment_bonus('agi')
    @property
    def total_vitality(self): return self.vitality + self._get_equipment_bonus('vit')
    @property
    def total_wisdom(self): return self.wisdom + self._get_equipment_bonus('wis')
    @property
    def total_discipline(self): return self.discipline + self._get_equipment_bonus('dis')
    @property
    def total_charisma(self): return self.charisma + self._get_equipment_bonus('cha')
    
    @property
    def equipment_xp_multiplier(self):
        mult = 1.0
        for inv in self.user.inventory.filter(equipped=True):
            if inv.item.metadata and isinstance(inv.item.metadata, dict):
                mult += (inv.item.metadata.get('bonus_xp_pct', 0) / 100.0)
        return mult
        
    @property
    def equipment_gold_multiplier(self):
        mult = 1.0
        for inv in self.user.inventory.filter(equipped=True):
            if inv.item.metadata and isinstance(inv.item.metadata, dict):
                mult += (inv.item.metadata.get('bonus_gold_pct', 0) / 100.0)
        return mult

    def __str__(self):
        return f"{self.user.username}'s Character - Lvl {self.level}"

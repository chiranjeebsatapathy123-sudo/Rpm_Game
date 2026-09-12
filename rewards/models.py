from django.db import models
from django.conf import settings

class GoldTransactionType(models.TextChoices):
    EARN = 'EARN', 'Earn'
    SPEND = 'SPEND', 'Spend'
    BONUS = 'BONUS', 'Bonus'
    REFUND = 'REFUND', 'Refund'

class ShopItemType(models.TextChoices):
    AVATAR = 'AVATAR', 'Avatar'
    FRAME = 'FRAME', 'Frame'
    THEME = 'THEME', 'Theme'
    TITLE = 'TITLE', 'Title'
    BADGE = 'BADGE', 'Badge'
    EFFECT = 'EFFECT', 'Effect'
    WEAPON = 'WEAPON', 'Weapon'
    ARMOR = 'ARMOR', 'Armor'
    ACCESSORY = 'ACCESSORY', 'Accessory'

class ShopItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    item_type = models.CharField(max_length=50, choices=ShopItemType.choices, default=ShopItemType.AVATAR)
    price = models.IntegerField()
    rarity = models.CharField(max_length=50, default='COMMON')
    icon = models.ImageField(upload_to='shop_icons/', null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.price} G)"

class GoldTransaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gold_transactions')
    amount = models.IntegerField()
    transaction_type = models.CharField(max_length=50, choices=GoldTransactionType.choices, default=GoldTransactionType.EARN)
    quest = models.ForeignKey('quests.Quest', on_delete=models.SET_NULL, null=True, blank=True, related_name='gold_transactions')
    shop_item = models.ForeignKey(ShopItem, on_delete=models.SET_NULL, null=True, blank=True, related_name='gold_transactions')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} | {self.amount} G | {self.transaction_type}"

class InventoryItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inventory')
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    equipped = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'item')

    def __str__(self):
        return f"{self.user.username} - {self.item.name}"

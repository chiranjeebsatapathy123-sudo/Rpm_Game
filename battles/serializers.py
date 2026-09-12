from rest_framework import serializers
from .models import Boss, PartyBattle, DamageLog
from social.serializers import PartySerializer

class BossSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boss
        fields = '__all__'

class DamageLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = DamageLog
        fields = '__all__'

class PartyBattleSerializer(serializers.ModelSerializer):
    boss = BossSerializer(read_only=True)
    party = PartySerializer(read_only=True)
    damage_logs = DamageLogSerializer(many=True, read_only=True)

    class Meta:
        model = PartyBattle
        fields = '__all__'

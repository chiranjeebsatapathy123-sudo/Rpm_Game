from rest_framework import serializers
from .models import Quest, Habit

class QuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = '__all__'
        read_only_fields = ['id', 'user', 'status', 'xp_reward', 'gold_reward', 'created_at', 'updated_at', 'completed_at']

    def validate(self, attrs):
        return attrs

class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['id', 'user', 'streak_count', 'last_completed_at', 'xp_reward', 'gold_reward', 'created_at', 'updated_at']

    def validate(self, attrs):
        return attrs

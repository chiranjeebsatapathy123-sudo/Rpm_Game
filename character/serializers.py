from rest_framework import serializers

from .models import Character


class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character

        fields = [
            "id",
            "user",
            "level",
            "total_xp",
            "gold",
            "health",
            "energy",
            "strength",
            "intellect",
            "agility",
            "vitality",
            "wisdom",
            "discipline",
            "charisma",
            "rpg_class",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "user",
            "level",
            "total_xp",
            "gold",
            "health",
            "energy",
            "strength",
            "intellect",
            "agility",
            "vitality",
            "wisdom",
            "discipline",
            "charisma",
            "created_at",
            "updated_at",
        ]
from rest_framework import serializers
from .models import Friendship, Party
from accounts.models import User

class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class FriendshipSerializer(serializers.ModelSerializer):
    user1 = UserSimpleSerializer(read_only=True)
    user2 = UserSimpleSerializer(read_only=True)
    user2_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Friendship
        fields = '__all__'
        read_only_fields = ['id', 'user1', 'status', 'created_at', 'updated_at']

class PartySerializer(serializers.ModelSerializer):
    leader = UserSimpleSerializer(read_only=True)
    members = UserSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Party
        fields = '__all__'
        read_only_fields = ['id', 'leader', 'created_at', 'members']

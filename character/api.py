from rest_framework import serializers, generics
from rest_framework.permissions import IsAuthenticated
from .models import Character

class CharacterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = '__all__'

class CharacterView(generics.RetrieveUpdateAPIView):
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        char, _ = Character.objects.get_or_create(user=self.request.user)
        return char

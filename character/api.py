from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Character
from .serializers import CharacterSerializer


class CharacterView(generics.RetrieveUpdateAPIView):
    serializer_class = CharacterSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        character, created = Character.objects.get_or_create(
            user=self.request.user
        )
        return character
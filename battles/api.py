from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Boss, PartyBattle, DamageLog
from .serializers import PartyBattleSerializer

class PartyBattleViewSet(viewsets.ModelViewSet):
    serializer_class = PartyBattleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PartyBattle.objects.filter(party__members=self.request.user).order_by('-started_at')

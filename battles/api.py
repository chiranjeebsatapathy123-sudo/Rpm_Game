from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import PartyBattle
from .serializers import PartyBattleSerializer


class PartyBattleViewSet(viewsets.ModelViewSet):
    serializer_class = PartyBattleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PartyBattle.objects.filter(
            party__members=self.request.user
        ).select_related(
            'party',
            'boss'
        ).order_by('-started_at')

    def perform_create(self, serializer):
        party = serializer.validated_data.get('party')

        if party is None:
            raise ValueError("A party is required.")

        if not party.members.filter(
            id=self.request.user.id
        ).exists():
            raise PermissionError(
                "You must be a member of the party to start a battle."
            )

        if not party.leader == self.request.user:
            raise PermissionError(
                "Only the party leader can start a battle."
            )

        if not serializer.validated_data.get('boss').active:
            raise ValueError(
                "This boss is not currently active."
            )

        serializer.save()

    def update(self, request, *args, **kwargs):
        battle = self.get_object()

        if battle.party.leader != request.user:
            return Response(
                {
                    "error": "Only the party leader can update a battle."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(
            request,
            *args,
            **kwargs
        )

    def partial_update(self, request, *args, **kwargs):
        battle = self.get_object()

        if battle.party.leader != request.user:
            return Response(
                {
                    "error": "Only the party leader can update a battle."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return super().partial_update(
            request,
            *args,
            **kwargs
        )

    def destroy(self, request, *args, **kwargs):
        battle = self.get_object()

        if battle.party.leader != request.user:
            return Response(
                {
                    "error": "Only the party leader can delete a battle."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(
            request,
            *args,
            **kwargs
        )
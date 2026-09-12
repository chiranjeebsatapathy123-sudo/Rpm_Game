from django.db.models import Q

from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Friendship, FriendshipStatus, Party
from .serializers import FriendshipSerializer, PartySerializer


class FriendshipViewSet(viewsets.ModelViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(
            Q(user1=self.request.user) |
            Q(user2=self.request.user)
        )

    def perform_create(self, serializer):
        user = self.request.user

        user2 = serializer.validated_data.get('user2')

        if user2 == user:
            raise serializers.ValidationError(
                "You cannot send a friend request to yourself."
            )

        existing = Friendship.objects.filter(
            Q(user1=user, user2=user2) |
            Q(user1=user2, user2=user)
        ).first()

        if existing:
            raise serializers.ValidationError(
                "A friendship or friend request already exists."
            )

        serializer.save(
            user1=user,
            status=FriendshipStatus.PENDING
        )

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friendship = self.get_object()

        if friendship.user2 != request.user:
            return Response(
                {
                    "error": "Only the receiver can accept the request."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        if friendship.status != FriendshipStatus.PENDING:
            return Response(
                {
                    "error": "This friend request is not pending."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        friendship.status = FriendshipStatus.ACCEPTED
        friendship.save(
            update_fields=['status']
        )

        return Response(
            {
                "status": "Friend request accepted."
            }
        )


class PartyViewSet(viewsets.ModelViewSet):
    serializer_class = PartySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Party.objects.filter(
            members=self.request.user
        )

    def perform_create(self, serializer):
        party = serializer.save(
            leader=self.request.user
        )

        party.members.add(
            self.request.user
        )

    def update(self, request, *args, **kwargs):
        party = self.get_object()

        if party.leader != request.user:
            return Response(
                {
                    "error": "Only the party leader can update the party."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(
            request,
            *args,
            **kwargs
        )

    def partial_update(self, request, *args, **kwargs):
        party = self.get_object()

        if party.leader != request.user:
            return Response(
                {
                    "error": "Only the party leader can update the party."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return super().partial_update(
            request,
            *args,
            **kwargs
        )

    def destroy(self, request, *args, **kwargs):
        party = self.get_object()

        if party.leader != request.user:
            return Response(
                {
                    "error": "Only the party leader can delete the party."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return super().destroy(
            request,
            *args,
            **kwargs
        )

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        try:
            party = Party.objects.get(pk=pk)
        except Party.DoesNotExist:
            return Response(
                {
                    "error": "Party not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if party.members.filter(
            id=request.user.id
        ).exists():
            return Response(
                {
                    "error": "You are already a member of this party."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        party.members.add(
            request.user
        )

        return Response(
            {
                "status": f"Joined party {party.name}."
            }
        )

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        party = self.get_object()

        if party.leader == request.user:
            return Response(
                {
                    "error": "The party leader cannot leave the party."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        party.members.remove(
            request.user
        )

        return Response(
            {
                "status": f"Left party {party.name}."
            }
        )
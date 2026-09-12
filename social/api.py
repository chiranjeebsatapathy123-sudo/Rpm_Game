from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Friendship, FriendshipStatus, Party
from .serializers import FriendshipSerializer, PartySerializer
from django.db.models import Q

class FriendshipViewSet(viewsets.ModelViewSet):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Friendship.objects.filter(Q(user1=self.request.user) | Q(user2=self.request.user))

    def perform_create(self, serializer):
        serializer.save(user1=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        friendship = self.get_object()
        if friendship.user2 != request.user:
            return Response({"error": "Only the receiver can accept the request."}, status=status.HTTP_403_FORBIDDEN)
        
        friendship.status = FriendshipStatus.ACCEPTED
        friendship.save()
        return Response({"status": "Friend request accepted."})

class PartyViewSet(viewsets.ModelViewSet):
    serializer_class = PartySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Party.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        party = serializer.save(leader=self.request.user)
        party.members.add(self.request.user)

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        party = self.get_object()
        party.members.add(request.user)
        return Response({"status": f"Joined party {party.name}."})

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Quest, Habit, QuestDifficulty, QuestStatus
from .serializers import QuestSerializer, HabitSerializer
from .services import complete_quest, complete_habit

def get_rewards(difficulty):
    xp_map = {QuestDifficulty.EASY: 20, QuestDifficulty.MEDIUM: 50, QuestDifficulty.HARD: 100, QuestDifficulty.EPIC: 250}
    gold_map = {QuestDifficulty.EASY: 10, QuestDifficulty.MEDIUM: 25, QuestDifficulty.HARD: 50, QuestDifficulty.EPIC: 125}
    return xp_map.get(difficulty, 50), gold_map.get(difficulty, 25)

class QuestViewSet(viewsets.ModelViewSet):
    serializer_class = QuestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Quest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        difficulty = serializer.validated_data.get('difficulty', QuestDifficulty.MEDIUM)
        xp, gold = get_rewards(difficulty)
        serializer.save(user=self.request.user, xp_reward=xp, gold_reward=gold)

    def perform_update(self, serializer):
        difficulty = serializer.validated_data.get('difficulty', serializer.instance.difficulty)
        xp, gold = get_rewards(difficulty)
        serializer.save(xp_reward=xp, gold_reward=gold)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        quest = self.get_object()
        try:
            result = complete_quest(request.user, quest)
            return Response(result)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An error occurred during completion."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        difficulty = serializer.validated_data.get('difficulty', QuestDifficulty.MEDIUM)
        xp, gold = get_rewards(difficulty)
        serializer.save(user=self.request.user, xp_reward=xp, gold_reward=gold)

    def perform_update(self, serializer):
        difficulty = serializer.validated_data.get('difficulty', serializer.instance.difficulty)
        xp, gold = get_rewards(difficulty)
        serializer.save(xp_reward=xp, gold_reward=gold)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        habit = self.get_object()
        try:
            result = complete_habit(request.user, habit)
            return Response(result)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An error occurred during completion."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from datetime import timedelta

from django.db.models import Count, Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from quests.models import Quest, Habit
from progression.models import XPTransaction


class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        try:
            char = user.character
            total_xp = char.total_xp
            total_gold = char.gold
        except Exception:
            total_xp = 0
            total_gold = 0

        quests_completed = Quest.objects.filter(
            user=user,
            status='COMPLETED'
        ).count()

        longest_streak = 0

        if hasattr(user, 'streak'):
            longest_streak = user.streak.longest_streak

        return Response({
            "total_xp": total_xp,
            "total_gold_earned": total_gold,
            "quests_completed": quests_completed,
            "longest_streak": longest_streak
        })


class AnalyticsDataAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        quest_categories = (
            Quest.objects
            .filter(user=user)
            .values('category')
            .annotate(count=Count('id'))
        )

        habit_categories = (
            Habit.objects
            .filter(user=user)
            .values('category')
            .annotate(count=Count('id'))
        )

        cat_data = {}

        for quest in quest_categories:
            category = quest['category']
            cat_data[category] = cat_data.get(
                category,
                0
            ) + quest['count']

        for habit in habit_categories:
            category = habit['category']
            cat_data[category] = cat_data.get(
                category,
                0
            ) + habit['count']

        category_labels = list(cat_data.keys())
        category_values = list(cat_data.values())

        # XP earned during the last 7 days.
        seven_days_ago = timezone.now() - timedelta(days=6)

        recent_xp = (
            XPTransaction.objects
            .filter(
                user=user,
                created_at__gte=seven_days_ago
            )
            .annotate(
                date=TruncDate('created_at')
            )
            .values('date')
            .annotate(
                total_xp=Sum('amount')
            )
            .order_by('date')
        )

        xp_by_date = {
            item['date']: item['total_xp'] or 0
            for item in recent_xp
        }

        trend_labels = []
        trend_xp = []

        for i in range(6, -1, -1):
            day = (
                timezone.now() - timedelta(days=i)
            ).date()

            trend_labels.append(
                day.strftime('%b %d')
            )

            trend_xp.append(
                xp_by_date.get(day, 0)
            )

        return Response({
            "categories": {
                "labels": category_labels,
                "values": category_values
            },
            "trends": {
                "labels": trend_labels,
                "xp": trend_xp
            }
        })
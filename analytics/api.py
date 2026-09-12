from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from quests.models import Quest, Habit
from character.models import Character
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from datetime import timedelta
from django.utils import timezone

class AnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # Calculate totals
        try:
            char = user.character
            total_xp = char.total_xp
            total_gold = char.gold
        except:
            total_xp = 0
            total_gold = 0
            
        quests_completed = Quest.objects.filter(user=user, status='COMPLETED').count()
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
        
        # 1. Category Breakdown (Active + Completed)
        quest_categories = Quest.objects.filter(user=user).values('category').annotate(count=Count('id'))
        habit_categories = Habit.objects.filter(user=user).values('category').annotate(count=Count('id'))
        
        cat_data = {}
        for q in quest_categories:
            cat_data[q['category']] = cat_data.get(q['category'], 0) + q['count']
        for h in habit_categories:
            cat_data[h['category']] = cat_data.get(h['category'], 0) + h['count']
            
        category_labels = list(cat_data.keys())
        category_values = list(cat_data.values())

        # 2. XP Trend (Last 7 Days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        
        recent_quests = Quest.objects.filter(
            user=user, 
            status='COMPLETED', 
            updated_at__gte=seven_days_ago
        ).annotate(
            date=TruncDate('updated_at')
        ).values('date').annotate(
            total_xp=Count('id') * 100 
        ).order_by('date')

        trend_labels = []
        trend_xp = []
        
        for i in range(6, -1, -1):
            day = (timezone.now() - timedelta(days=i)).date()
            trend_labels.append(day.strftime('%b %d'))
            
            day_data = next((item for item in recent_quests if item['date'] == day), None)
            if day_data:
                trend_xp.append(day_data['total_xp'])
            else:
                trend_xp.append(0)

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

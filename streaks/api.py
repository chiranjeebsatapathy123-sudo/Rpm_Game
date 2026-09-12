from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class StreakView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if hasattr(user, 'streak'):
            return Response({
                "current_streak": user.streak.current_streak,
                "longest_streak": user.streak.longest_streak,
                "last_activity_date": user.streak.last_activity_date
            })
        return Response({"current_streak": 0, "longest_streak": 0, "last_activity_date": None})

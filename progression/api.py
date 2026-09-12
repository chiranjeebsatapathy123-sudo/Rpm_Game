from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import xp_for_next_level, current_level_xp, level_progress

class ProgressionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'character'):
            return Response({"error": "Character not found"}, status=404)
            
        character = user.character
        total_xp = character.total_xp
        
        return Response({
            "level": character.level,
            "total_xp": total_xp,
            "current_level_xp": current_level_xp(total_xp),
            "xp_for_next_level": xp_for_next_level(character.level),
            "progress_percent": round(level_progress(total_xp) * 100, 2)
        })

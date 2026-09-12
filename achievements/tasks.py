from celery import shared_task
from .services import check_achievements
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def process_achievements_task(user_id):
    try:
        user = User.objects.get(id=user_id)
        check_achievements(user)
    except User.DoesNotExist:
        pass

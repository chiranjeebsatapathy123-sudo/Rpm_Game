from celery import shared_task
from .models import WebhookToken, IntegrationRule
from quests.services import complete_quest, complete_habit

@shared_task
def process_webhook_rules_task(token_id, event):
    try:
        token = WebhookToken.objects.get(id=token_id, is_active=True)
        user = token.user
        
        rules = IntegrationRule.objects.filter(token=token, source_event=event)
        
        for rule in rules:
            if rule.target_quest and rule.target_quest.status != 'COMPLETED':
                try:
                    complete_quest(user, rule.target_quest)
                except Exception as e:
                    pass
            
            if rule.target_habit:
                try:
                    complete_habit(user, rule.target_habit)
                except Exception as e:
                    pass
    except WebhookToken.DoesNotExist:
        pass

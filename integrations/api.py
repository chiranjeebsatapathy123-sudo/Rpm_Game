from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import WebhookToken, IntegrationRule
from quests.services import complete_quest, complete_habit
from .serializers import WebhookTokenSerializer, IntegrationRuleSerializer

class WebhookTokenViewSet(viewsets.ModelViewSet):
    serializer_class = WebhookTokenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WebhookToken.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class IntegrationRuleViewSet(viewsets.ModelViewSet):
    serializer_class = IntegrationRuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IntegrationRule.objects.filter(token__user=self.request.user)

class WebhookReceiverAPIView(APIView):
    permission_classes = [] # Allow unauthenticated access since we use token in URL/header

    def post(self, request, token_str):
        # 1. Find token
        token = get_object_or_404(WebhookToken, token=token_str, is_active=True)
        user = token.user

        # 2. Extract event type. We'll look for an 'event' key in JSON payload.
        event = request.data.get('event')
        if not event:
            return Response({"error": "Missing 'event' in payload"}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Find matching rules
        rules = IntegrationRule.objects.filter(token=token, source_event=event)
        if not rules.exists():
            return Response({"message": f"No rules configured for event: {event}"}, status=status.HTTP_200_OK)

        # 4. Execute rules asynchronously via Celery
        from .tasks import process_webhook_rules_task
        process_webhook_rules_task.delay(token.id, event)

        return Response({"message": "Webhook received and processing started."}, status=status.HTTP_202_ACCEPTED)

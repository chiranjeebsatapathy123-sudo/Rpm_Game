import logging

from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import WebhookToken, IntegrationRule
from .serializers import WebhookTokenSerializer, IntegrationRuleSerializer


logger = logging.getLogger(__name__)


class WebhookTokenViewSet(viewsets.ModelViewSet):
    serializer_class = WebhookTokenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WebhookToken.objects.filter(
            user=self.request.user
        ).prefetch_related('rules')

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )

    def perform_update(self, serializer):
        token = self.get_object()

        if token.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You do not have permission to modify this token."
            )

        serializer.save()


class IntegrationRuleViewSet(viewsets.ModelViewSet):
    serializer_class = IntegrationRuleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IntegrationRule.objects.filter(
            token__user=self.request.user
        ).select_related(
            'token',
            'target_quest',
            'target_habit'
        )

    def perform_create(self, serializer):
        token = serializer.validated_data.get('token')
        target_quest = serializer.validated_data.get('target_quest')
        target_habit = serializer.validated_data.get('target_habit')

        if token is None:
            raise ValueError("A webhook token is required.")

        if token.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You cannot use another user's webhook token."
            )

        if target_quest is not None:
            if target_quest.user != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied(
                    "You cannot connect another user's quest."
                )

        if target_habit is not None:
            if target_habit.user != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied(
                    "You cannot connect another user's habit."
                )

        if target_quest is None and target_habit is None:
            raise ValueError(
                "A rule must target either a quest or a habit."
            )

        serializer.save()

    def perform_update(self, serializer):
        token = serializer.validated_data.get(
            'token',
            serializer.instance.token
        )

        target_quest = serializer.validated_data.get(
            'target_quest',
            serializer.instance.target_quest
        )

        target_habit = serializer.validated_data.get(
            'target_habit',
            serializer.instance.target_habit
        )

        if token.user != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "You cannot use another user's webhook token."
            )

        if target_quest is not None:
            if target_quest.user != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied(
                    "You cannot connect another user's quest."
                )

        if target_habit is not None:
            if target_habit.user != self.request.user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied(
                    "You cannot connect another user's habit."
                )

        if target_quest is None and target_habit is None:
            raise ValueError(
                "A rule must target either a quest or a habit."
            )

        serializer.save()


class WebhookReceiverAPIView(APIView):
    permission_classes = []

    def post(self, request, token_str):
        token = get_object_or_404(
            WebhookToken,
            token=token_str,
            is_active=True
        )

        event = request.data.get('event')

        if not event:
            return Response(
                {
                    "error": "Missing 'event' in payload."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        rules = IntegrationRule.objects.filter(
            token=token,
            source_event=event
        )

        if not rules.exists():
            return Response(
                {
                    "message": f"No rules configured for event: {event}"
                },
                status=status.HTTP_200_OK
            )

        try:
            from .tasks import process_webhook_rules_task

            process_webhook_rules_task.delay(
                token.id,
                event
            )

        except Exception:
            logger.exception(
                "Failed to queue webhook task for token %s and event %s",
                token.id,
                event
            )

            return Response(
                {
                    "error": "Webhook processing could not be started."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(
            {
                "message": "Webhook received and processing started."
            },
            status=status.HTTP_202_ACCEPTED
        )
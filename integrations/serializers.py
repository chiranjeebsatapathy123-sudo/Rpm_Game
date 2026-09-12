from rest_framework import serializers
from .models import WebhookToken, IntegrationRule

class IntegrationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntegrationRule
        fields = '__all__'

class WebhookTokenSerializer(serializers.ModelSerializer):
    rules = IntegrationRuleSerializer(many=True, read_only=True)
    class Meta:
        model = WebhookToken
        fields = '__all__'
        read_only_fields = ['user', 'token']

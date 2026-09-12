from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.api import RegisterView, LogoutView, UserMeView
from quests.api import QuestViewSet, HabitViewSet
from character.api import CharacterView
from rewards.api import ShopViewSet, InventoryViewSet
from achievements.api import AchievementViewSet
from analytics.api import AnalyticsView
from streaks.api import StreakView
from notifications.api import NotificationViewSet
from progression.api import ProgressionView
from social.api import FriendshipViewSet, PartyViewSet
from integrations.api import WebhookReceiverAPIView, WebhookTokenViewSet, IntegrationRuleViewSet
from battles.api import PartyBattleViewSet
from analytics.api import AnalyticsDataAPIView

router = DefaultRouter()
router.register(r'quests', QuestViewSet, basename='quest')
router.register(r'habits', HabitViewSet, basename='habit')
router.register(r'shop', ShopViewSet, basename='shop')
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'friendships', FriendshipViewSet, basename='friendship')
router.register(r'parties', PartyViewSet, basename='party')
router.register(r'battles', PartyBattleViewSet, basename='battle')
router.register(r'webhook-tokens', WebhookTokenViewSet, basename='webhook-token')
router.register(r'integration-rules', IntegrationRuleViewSet, basename='integration-rule')

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='auth_login'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='auth_refresh'),
    path('auth/me/', UserMeView.as_view(), name='auth_me'),
    
    # Webhooks
    path('webhooks/<str:token_str>/', WebhookReceiverAPIView.as_view(), name='webhook_receiver'),
    
    # Character & Progression
    path('character/', CharacterView.as_view(), name='character_api'),
    path('progression/', ProgressionView.as_view(), name='progression_api'),
    path('streak/', StreakView.as_view(), name='streak_api'),
    path('analytics/', AnalyticsView.as_view(), name='analytics_api'),
    path('analytics/charts/', AnalyticsDataAPIView.as_view(), name='analytics_charts_api'),
    
    # App routers
    path('', include(router.urls)),
]

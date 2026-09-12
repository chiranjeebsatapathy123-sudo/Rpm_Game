from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('onboarding/', views.onboarding_view, name='onboarding'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('quests/', views.quests_view, name='quests'),
    path('character/', views.character_view, name='character'),
    path('achievements/', views.achievements_view, name='achievements'),
    path('shop/', views.shop_view, name='shop'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('social/', views.social_view, name='social'),
    path('battles/', include('battles.urls')),
    path('integrations/', include('integrations.urls')),
    path('settings/', views.settings_view, name='settings'),
]

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User
from character.models import Character
from quests.models import Quest, QuestDifficulty, QuestStatus

class QuestTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@test.com')
        self.character = Character.objects.create(user=self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.quest = Quest.objects.create(
            user=self.user,
            title="Test Quest",
            difficulty=QuestDifficulty.EASY,
            xp_reward=20,
            gold_reward=10
        )

    def test_quest_creation(self):
        self.assertEqual(Quest.objects.count(), 1)
        self.assertEqual(self.quest.status, QuestStatus.TODO)

    def test_quest_completion(self):
        # Using the complete API endpoint
        url = reverse('quest-complete', kwargs={'pk': self.quest.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, 200)
        self.quest.refresh_from_db()
        self.character.refresh_from_db()
        
        self.assertEqual(self.quest.status, QuestStatus.COMPLETED)
        self.assertEqual(self.character.total_xp, 20)
        self.assertEqual(self.character.gold, 110) # Base 100 + 10

    def test_duplicate_completion_prevented(self):
        url = reverse('quest-complete', kwargs={'pk': self.quest.pk})
        self.client.post(url) # First complete
        
        # Second complete
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'Quest is already completed.')

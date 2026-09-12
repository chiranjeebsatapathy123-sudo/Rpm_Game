from django.test import TestCase
from progression.services import calculate_level, xp_for_level

class ProgressionTests(TestCase):
    def test_level_1_xp(self):
        self.assertEqual(calculate_level(0), 1)
        self.assertEqual(calculate_level(50), 1)

    def test_level_2_xp(self):
        # Formula: 100 * (1 ** 1.6) = 100 to go from 1 to 2
        # Total XP needed to reach Level 2 is 100
        self.assertEqual(xp_for_level(2), 100)
        self.assertEqual(calculate_level(100), 2)
        self.assertEqual(calculate_level(150), 2)

    def test_level_3_xp(self):
        # Level 1->2: 100
        # Level 2->3: round(100 * (2 ** 1.6)) = round(100 * 3.0314) = 303
        # Total XP needed to reach Level 3: 100 + 303 = 403
        self.assertEqual(xp_for_level(3), 403)
        self.assertEqual(calculate_level(403), 3)
        self.assertEqual(calculate_level(500), 3)

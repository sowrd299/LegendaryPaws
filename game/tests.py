from django.test import TestCase, Client
from django.urls import reverse
from game.engine import (
    raw_to_scaled, Character, Party, CombatEngine, CARDS, create_initial_game_state
)
from game.views import generate_random_enemies

class EngineTests(TestCase):
    def test_raw_to_scaled_formula(self):
        """Test triangular 0 to 20 stat scaling formula."""
        self.assertEqual(raw_to_scaled(0), 0)
        self.assertEqual(raw_to_scaled(1), 1)  # 1:1 for the first level
        self.assertEqual(raw_to_scaled(3), 2)  # +2 raw needed for level 2
        self.assertEqual(raw_to_scaled(6), 3)  # +3 raw needed for level 3
        self.assertEqual(raw_to_scaled(10), 4) # +4 raw needed for level 4
        self.assertEqual(raw_to_scaled(15), 5) # +5 raw needed for level 5
        self.assertEqual(raw_to_scaled(55), 10) # +10 raw needed for level 10
        self.assertEqual(raw_to_scaled(210), 20) # Max 20 reached at 210 raw
        self.assertEqual(raw_to_scaled(300), 20) # Caps at 20

    def test_all_stats_equally_scaled_including_haleness_and_hp(self):
        """Verify scaling applies equally to all stats, including haleness & HP."""
        hero = Character(name="TestHero", species="Fox", current_class="Wandering Spellsword", level=1)
        raw_stats = hero.get_raw_stats()
        scaled_stats = hero.get_scaled_stats()

        # Check all accessible stats follow raw_to_scaled
        for stat, raw_val in raw_stats.items():
            if stat in hero.get_accessible_stats():
                expected_scaled = raw_to_scaled(raw_val)
                self.assertEqual(scaled_stats[stat], expected_scaled)

        # Check haleness is in scaled stats and used for max_hp
        self.assertIn('haleness', scaled_stats)
        expected_haleness = raw_to_scaled(raw_stats['haleness'])
        self.assertEqual(scaled_stats['haleness'], expected_haleness)
        self.assertEqual(hero.max_hp, max(10, 10 + expected_haleness * 2))

    def test_character_creation_and_leveling(self):
        """Test character stats calculation and giving level-up cards."""
        hero = Character(name="TestHero", species="Fox", current_class="Wandering Spellsword", level=1)
        scaled_stats = hero.get_scaled_stats()
        self.assertIn('brute_intensity', scaled_stats)
        self.assertGreaterEqual(scaled_stats['brute_intensity'], 0)
        self.assertLessEqual(scaled_stats['brute_intensity'], 20)

        # Give card to boost stat & level
        success, msg = hero.give_card('Slash')
        self.assertTrue(success)
        self.assertEqual(hero.level, 2)
        self.assertIn('Slash', hero.level_up_cards)

    def test_level_tracked_as_stat(self):
        """Verify level is tracked as a stat using existing stat-scaling logic and raw card contributions."""
        hero = Character(name="TestHero", species="Fox", current_class="Wandering Spellsword", level=1)
        self.assertIn('level', hero.get_accessible_stats())
        self.assertEqual(hero.get_raw_stats()['level'], 1.0)
        self.assertEqual(hero.level, 1)

        # Giving 1 card adds 1 to raw level value (raw level becomes 2.0 -> scaled level 2)
        hero.give_card('Slash')
        self.assertEqual(hero.get_raw_stats()['level'], 2.0)
        self.assertEqual(hero.level, 2)

        # Giving 2 more cards makes raw level = 4.0 -> scaled level is 2
        hero.give_card('Honed Slash')
        hero.give_card('First aid')
        self.assertEqual(hero.get_raw_stats()['level'], 4.0)
        self.assertEqual(hero.level, 2)

        # Giving a 4th card makes raw level = 5.0 -> raw_to_scaled(5.0) = 3
        hero.give_card('Wain')
        self.assertEqual(hero.get_raw_stats()['level'], 5.0)
        self.assertEqual(hero.level, 3)

    def test_enemy_generation_system(self):
        """Verify enemies are created using the exact same Character system."""
        enemies = generate_random_enemies('^', level=2)
        self.assertGreaterEqual(len(enemies), 1)
        for enemy in enemies:
            self.assertIsInstance(enemy, Character)
            self.assertEqual(enemy.level, 2)
            self.assertTrue(enemy.is_alive())

    def test_combat_engine_wait_and_attack(self):
        """Test turn-based combat engine with Wait card and Slash attack."""
        hero = Character(name="Hero", species="Fox", current_class="Squire", level=1)
        enemy = Character(name="Wild Cat", species="Cat", current_class="Scout", level=1)
        
        engine = CombatEngine([hero], [enemy])
        self.assertFalse(engine.is_over)

        # Player turn: Execute Wait action
        engine.execute_player_turn(hero, 'Wait', hero.id)
        self.assertTrue(hero.is_alive())

        # Player turn: Attack enemy with Slash
        initial_hp = enemy.current_hp
        engine.execute_player_turn(hero, 'Slash', enemy.id)
        self.assertLessEqual(enemy.current_hp, initial_hp)


class ViewIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_game_index_initial_state(self):
        """Test initial game load starts at Voinara intro screen."""
        response = self.client.get(reverse('game_index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Voinara:")

    def test_voinara_dialogue_progression(self):
        """Test advancing Voinara dialogue lines."""
        response = self.client.post(reverse('handle_action'), {'action_type': 'voinara_advance'})
        self.assertEqual(response.status_code, 302)
        
        # Follow redirect to game_index
        response = self.client.get(reverse('game_index'))
        self.assertEqual(response.status_code, 200)

    def test_overworld_movement(self):
        """Test moving on overworld grid."""
        # Fast forward past Voinara intro
        session = self.client.session
        state = create_initial_game_state()
        state['screen'] = 'overworld'
        session['game_state'] = state
        session.save()

        response = self.client.post(reverse('handle_action'), {
            'action_type': 'move',
            'direction': 'left'
        })
        self.assertEqual(response.status_code, 302)

        # Verify position changed in session
        updated_state = self.client.session['game_state']
        updated_party = Party.from_dict(updated_state['party'])
        self.assertEqual(updated_party.x, 6)

    def test_reset_session_clears_session_data(self):
        """Test visiting secret reset page clears game_state and session."""
        session = self.client.session
        state = create_initial_game_state()
        state['screen'] = 'overworld'
        state['voinara_step'] = 5
        session['game_state'] = state
        session.save()

        response = self.client.get(reverse('reset_session'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Session Reset")
        self.assertContains(response, "Game session has been reset successfully")
        self.assertNotIn('game_state', self.client.session)

        # Confirm returning to index starts fresh intro
        index_response = self.client.get(reverse('game_index'))
        self.assertEqual(index_response.status_code, 200)
        self.assertContains(index_response, "Voinara:")


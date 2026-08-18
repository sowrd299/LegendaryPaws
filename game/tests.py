from django.test import TestCase, Client
from django.urls import reverse
from game.engine import (
    raw_to_scaled, Character, Party, CombatEngine, CARDS, create_initial_game_state
)
from game.map import generate_random_enemies, DEFAULT_CHARACTER_NAMES

class EngineTests(TestCase):
    def test_character_generation_default_names(self):
        """Test character generation picks names from DEFAULT_CHARACTER_NAMES including Twig and Lily."""
        encounter_data = {
            'min_enemies': 2,
            'max_enemies': 2,
            'species': ['Fox', 'Cat'],
            'classes': ['Student', 'Squire'],
        }
        enemies = generate_random_enemies(encounter_data)
        self.assertEqual(len(enemies), 2)
        for enemy in enemies:
            self.assertIn(enemy.name, DEFAULT_CHARACTER_NAMES)

    def test_character_generation_per_encounter_names(self):
        """Test character generation uses per-encounter custom names list if provided."""
        custom_names = ['CustomTwig', 'CustomLily']
        encounter_data = {
            'min_enemies': 2,
            'max_enemies': 2,
            'species': ['Fox'],
            'classes': ['Student'],
            'names': custom_names
        }
        enemies = generate_random_enemies(encounter_data)
        self.assertEqual(len(enemies), 2)
        enemy_names = [e.name for e in enemies]
        self.assertIn('CustomTwig', enemy_names)
        self.assertIn('CustomLily', enemy_names)

    def test_raw_to_scaled_formula(self):
        """Test square-root 0 to 20 stat scaling formula."""
        self.assertEqual(raw_to_scaled(0), 0)
        self.assertEqual(raw_to_scaled(1), 1)
        self.assertEqual(raw_to_scaled(4), 2)
        self.assertEqual(raw_to_scaled(9), 3)
        self.assertEqual(raw_to_scaled(16), 4)
        self.assertEqual(raw_to_scaled(100), 10)
        self.assertEqual(raw_to_scaled(400), 20)
        self.assertEqual(raw_to_scaled(500), 20)

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

        # Give cards to boost stat & level (5 cards with 0.4 level boost each to reach raw level 4 -> scaled level 2)
        for _ in range(4):
            hero.give_card('Slash')
        success, msg = hero.give_card('Slash')
        self.assertTrue(success)
        self.assertEqual(hero.get_scaled_stats().get('level'), 2)
        self.assertIn('Slash', hero.level_up_cards)

    def test_level_tracked_as_stat(self):
        """Verify level is tracked as a stat using existing stat-scaling logic and raw card contributions."""
        hero = Character(name="TestHero", species="Fox", current_class="Wandering Spellsword", level=1)
        self.assertIn('level', hero.get_accessible_stats())
        self.assertEqual(hero.get_raw_stats()['level'], 2.0)
        self.assertEqual(hero.get_scaled_stats().get('level'), 1)

        # Giving 5 cards with 0.4 level boost each adds 2.0 to raw level value (raw level becomes 4.0 -> scaled level 2)
        for _ in range(5):
            hero.give_card('Slash')
        self.assertEqual(hero.get_raw_stats()['level'], 4.0)
        self.assertEqual(hero.get_scaled_stats().get('level'), 2)

        # Giving 13 more cards makes raw level = 9.2 -> raw_to_scaled(9.2) = 3
        for _ in range(13):
            hero.give_card('Slash')
        self.assertEqual(hero.get_scaled_stats().get('level'), 3)

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

    def test_recruitable_enemy_generation_and_gear(self):
        """Test enemy generation with cards_by_class and target_level boosting."""
        encounter_data = {
            'min_enemies': 1,
            'max_enemies': 1,
            'species': ['Fox'],
            'classes': ['Student'],
            'target_level': 2,
            'is_recruitable': True,
            'cards_by_class': {
                'Student': {
                    'trinket': ['Study'],
                    'scroll': ['Elementary Magic'],
                    'weapon': ['Slash'],
                    'armor': ['Light Clothes'],
                }
            }
        }
        enemies = generate_random_enemies(encounter_data)
        self.assertEqual(len(enemies), 1)
        enemy = enemies[0]
        self.assertEqual(enemy.species, 'Fox')
        self.assertEqual(enemy.current_class, 'Student')
        self.assertGreaterEqual(enemy.get_scaled_stats().get('level'), 2)

    def test_combat_engine_recruitment_logic(self):
        """Test that Bargain card marks enemy as is_recruited only when is_recruitable is True."""
        hero = Character(name="Hero", species="Fox", current_class="Squire", level=1)
        enemy = Character(name="Student Enemy", species="Cat", current_class="Student", level=1)
        enemy.current_hp = 1

        # Non-recruitable encounter
        engine1 = CombatEngine([hero], [enemy], is_recruitable=False)
        engine1.execute_player_turn(hero, 'Bargain', enemy.id)
        self.assertFalse(enemy.is_alive())
        self.assertFalse(getattr(enemy, 'is_recruited', False))

        # Recruitable encounter
        enemy2 = Character(name="Student Enemy 2", species="Cat", current_class="Student", level=1)
        enemy2.current_hp = 1
        engine2 = CombatEngine([hero], [enemy2], is_recruitable=True)
        engine2.execute_player_turn(hero, 'Bargain', enemy2.id)
        self.assertFalse(enemy2.is_alive())
        self.assertTrue(getattr(enemy2, 'is_recruited', False))


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

    def test_combat_end_recruitment_victory(self):
        """Test combat_end victory adds recruited enemy to party when room is available."""
        session = self.client.session
        state = create_initial_game_state()
        party = Party.from_dict(state['party'])
        self.assertEqual(len(party.members), 1)

        recruited_enemy = Character(name="Recruited Cat", species="Cat", current_class="Student", level=1)
        recruited_enemy.is_recruited = True
        recruited_enemy.current_hp = 0

        engine = CombatEngine(party.members, [recruited_enemy], is_recruitable=True)
        engine.is_over = True
        engine.victory = True
        state['combat'] = engine.to_dict()
        state['screen'] = 'combat'
        session['game_state'] = state
        session.save()

        response = self.client.post(reverse('handle_action'), {'action_type': 'combat_end'})
        self.assertEqual(response.status_code, 302)

        updated_state = self.client.session['game_state']
        updated_party = Party.from_dict(updated_state['party'])
        self.assertEqual(len(updated_party.members), 2)
        self.assertEqual(updated_party.members[1].name, "Recruited Cat")



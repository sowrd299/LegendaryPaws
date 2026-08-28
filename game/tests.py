# NOTE FOR TEST MAINTAINERS:
# Avoid hardcoding exact map coordinates or content strings that are not explicitly provided within
# the test cases themselves. Game content and layout will update frequently, so tests should look up
# data dynamically (e.g. using get_inn_coords or helper functions) rather than using fixed magic numbers.

from django.test import TestCase, Client
from django.urls import reverse
from game.engine import (
    raw_to_scaled, Character, Party, CombatEngine, CARDS, create_initial_game_state
)
from game.map import (
    generate_random_enemies, DEFAULT_CHARACTER_NAMES, get_inn_id, get_inn, get_nearest_inn_id,
    calculate_map_pan, DEFAULT_START_INN_ID, get_inn_coords
)

class EngineTests(TestCase):
    def test_inn_reading_order_and_nearest_resolution(self):
        """Test reading-order ID assignment and nearest Inn resolution."""
        start_x, start_y = get_inn_coords(DEFAULT_START_INN_ID)
        inn_id = get_inn_id(start_x, start_y)
        self.assertEqual(inn_id, DEFAULT_START_INN_ID)

        inn_data = get_inn(start_x, start_y)
        self.assertIsNotNone(inn_data)
        self.assertEqual(inn_data['id'], DEFAULT_START_INN_ID)

        nearest = get_nearest_inn_id(start_x, start_y)
        self.assertEqual(nearest, DEFAULT_START_INN_ID)

    def test_character_generation_default_names(self):
        """Test character generation picks names from DEFAULT_CHARACTER_NAMES including Twig and Lily."""
        encounter_data = {
            'min_enemies': 2,
            'max_enemies': 2,
            'species': ['Fox', 'Cat'],
            'classes': ['Student', 'Squire'],
            'names': DEFAULT_CHARACTER_NAMES,
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
        """Test initial game load starts at Voinara intro quest on dialog screen."""
        response = self.client.get(reverse('game_index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['screen'], 'dialog')
        self.assertContains(response, "Voinara:")

    def test_voinara_dialogue_progression(self):
        """Test advancing Voinara dialogue lines using dialog_advance."""
        # 4 lines total for voinara_intro quest
        for _ in range(4):
            response = self.client.post(reverse('handle_action'), {'action_type': 'dialog_advance'})
            self.assertEqual(response.status_code, 302)

        # After 4th advance, screen returns to overworld
        response = self.client.get(reverse('game_index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['screen'], 'overworld')

    def test_overworld_movement(self):
        """Test moving on overworld grid."""
        # Fast forward past Voinara intro
        session = self.client.session
        state = create_initial_game_state()
        state['screen'] = 'overworld'
        state['active_dialogue'] = None
        state['quests']['voinara_intro'] = 1
        session['game_state'] = state
        initial_party = Party.from_dict(state['party'])
        initial_x = initial_party.x

        response = self.client.post(reverse('handle_action'), {
            'action_type': 'move',
            'direction': 'left'
        })
        self.assertEqual(response.status_code, 302)

        # Verify position changed in session
        updated_state = self.client.session['game_state']
        updated_party = Party.from_dict(updated_state['party'])
        self.assertEqual(updated_party.x, initial_x - 1)

    def test_reset_session_clears_session_data(self):
        """Test visiting secret reset page clears game_state and session."""
        session = self.client.session
        state = create_initial_game_state()
        state['screen'] = 'overworld'
        state['active_dialogue'] = None
        state['quests']['voinara_intro'] = 1
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
        self.assertEqual(index_response.context['screen'], 'dialog')
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

    def test_combat_end_recruitment_overflow_to_inn(self):
        """Test combat_end victory sends recruited enemy to nearest inn when party is full (4 members)."""
        session = self.client.session
        state = create_initial_game_state()
        party = Party.from_dict(state['party'])
        for i in range(3):
            party.members.append(Character(name=f"Member {i+2}", species="Fox", current_class="Squire"))
        self.assertEqual(len(party.members), 4)

        recruited_enemy = Character(name="Overflow Owl", species="Owl", current_class="Student", level=1)
        recruited_enemy.is_recruited = True
        recruited_enemy.current_hp = 0

        engine = CombatEngine(party.members, [recruited_enemy], is_recruitable=True)
        engine.is_over = True
        engine.victory = True
        state['combat'] = engine.to_dict()
        state['screen'] = 'combat'
        state['party'] = party.to_dict()
        session['game_state'] = state
        session.save()

        response = self.client.post(reverse('handle_action'), {'action_type': 'combat_end'})
        self.assertEqual(response.status_code, 302)

        updated_state = self.client.session['game_state']
        updated_party = Party.from_dict(updated_state['party'])
        self.assertEqual(len(updated_party.members), 4)
        
        inns = updated_state.get('inns', {})
        self.assertIn('inn_0', inns)
        inn_0_chars = inns['inn_0']
        self.assertEqual(len(inn_0_chars), 1)
        self.assertEqual(inn_0_chars[0]['name'], "Overflow Owl")

    def test_inn_recruit_action_success_and_party_full(self):
        """Test recruiting guest from Inn to party, and blocking recruitment when party is full (4)."""
        session = self.client.session
        state = create_initial_game_state()
        state['current_inn_id'] = 'inn_0'
        guest = Character(name="Inn Guest Cat", species="Cat", current_class="Student", level=1)
        state['inns'] = {'inn_0': [guest.to_dict()]}
        session['game_state'] = state
        session.save()

        # Recruit guest into party (1 -> 2 members)
        response = self.client.post(reverse('handle_action'), {
            'action_type': 'inn_recruit',
            'char_index': 0
        })
        self.assertEqual(response.status_code, 302)

        updated_state = self.client.session['game_state']
        updated_party = Party.from_dict(updated_state['party'])
        self.assertEqual(len(updated_party.members), 2)
        self.assertEqual(updated_party.members[1].name, "Inn Guest Cat")
        self.assertEqual(len(updated_state['inns']['inn_0']), 0)

        # Fill party to 4 members & add another guest to inn
        updated_party.members.append(Character(name="Member 3", species="Fox", current_class="Squire"))
        updated_party.members.append(Character(name="Member 4", species="Badger", current_class="Scout"))
        guest2 = Character(name="Extra Guest", species="Rabbit", current_class="Student")
        updated_state['inns']['inn_0'] = [guest2.to_dict()]
        updated_state['party'] = updated_party.to_dict()
        session['game_state'] = updated_state
        session.save()

        # Attempt to recruit 5th member
        response = self.client.post(reverse('handle_action'), {
            'action_type': 'inn_recruit',
            'char_index': 0
        })
        self.assertEqual(response.status_code, 302)
        final_state = self.client.session['game_state']
        final_party = Party.from_dict(final_state['party'])
        self.assertEqual(len(final_party.members), 4)

    def test_inn_dismiss_action_success_and_min_party_limit(self):
        """Test dismissing party member to Inn, and preventing dismissal when only 1 member remains."""
        session = self.client.session
        state = create_initial_game_state()
        state['current_inn_id'] = 'inn_0'
        party = Party.from_dict(state['party'])
        companion = Character(name="Party Companion", species="Owl", current_class="Scout")
        party.members.append(companion)
        state['party'] = party.to_dict()
        session['game_state'] = state
        session.save()

        # Dismiss companion (2 -> 1 member)
        response = self.client.post(reverse('handle_action'), {
            'action_type': 'inn_dismiss',
            'char_index': 1
        })
        self.assertEqual(response.status_code, 302)

        updated_state = self.client.session['game_state']
        updated_party = Party.from_dict(updated_state['party'])
        self.assertEqual(len(updated_party.members), 1)
        self.assertEqual(len(updated_state['inns']['inn_0']), 1)
        self.assertEqual(updated_state['inns']['inn_0'][0]['name'], "Party Companion")

        response = self.client.post(reverse('handle_action'), {
            'action_type': 'inn_dismiss',
            'char_index': 0
        })
        self.assertEqual(response.status_code, 302)
        final_state = self.client.session['game_state']
        final_party = Party.from_dict(final_state['party'])
        self.assertEqual(len(final_party.members), 1)

    def test_start_position_at_default_inn(self):
        """Test initial game state sets party start position and respawn_inn_id to DEFAULT_START_INN_ID."""
        state = create_initial_game_state()
        party = Party.from_dict(state['party'])
        expected_x, expected_y = get_inn_coords(DEFAULT_START_INN_ID)
        self.assertEqual(party.x, expected_x)
        self.assertEqual(party.y, expected_y)
        self.assertEqual(state.get('respawn_inn_id'), DEFAULT_START_INN_ID)

    def test_visiting_inn_updates_respawn_inn_id(self):
        """Test visiting an inn updates respawn_inn_id in game state."""
        session = self.client.session
        state = create_initial_game_state()
        state['screen'] = 'overworld'
        
        # Position party adjacent to an inn tile and move onto it
        inn_x, inn_y = get_inn_coords(DEFAULT_START_INN_ID)
        party = Party.from_dict(state['party'])
        party.x = inn_x - 1
        party.y = inn_y
        state['party'] = party.to_dict()
        session['game_state'] = state
        session.save()

        response = self.client.post(reverse('handle_action'), {
            'action_type': 'move',
            'direction': 'right'
        })
        self.assertEqual(response.status_code, 302)

        updated_state = self.client.session['game_state']
        self.assertEqual(updated_state.get('respawn_inn_id'), DEFAULT_START_INN_ID)

    def test_combat_defeat_respawns_at_respawn_inn_position(self):
        """Test combat defeat respawns party at the coordinates of respawn_inn_id."""
        session = self.client.session
        state = create_initial_game_state()
        state['screen'] = 'combat'
        state['respawn_inn_id'] = DEFAULT_START_INN_ID
        
        party = Party.from_dict(state['party'])
        party.x = 0
        party.y = 0
        
        enemy = Character(name="Defeating Enemy", species="Fox", current_class="Squire")
        engine = CombatEngine(party.members, [enemy])
        engine.is_over = True
        engine.victory = False
        
        state['combat'] = engine.to_dict()
        state['party'] = party.to_dict()
        session['game_state'] = state
        session.save()

        response = self.client.post(reverse('handle_action'), {'action_type': 'combat_end'})
        self.assertEqual(response.status_code, 302)

        updated_state = self.client.session['game_state']
        updated_party = Party.from_dict(updated_state['party'])
        expected_x, expected_y = get_inn_coords(DEFAULT_START_INN_ID)
        self.assertEqual(updated_party.x, expected_x)
        self.assertEqual(updated_party.y, expected_y)


from game.map import (
    MapZone, MAP_ZONES, get_tile, get_tile_description,
    get_map_min_x, get_map_min_y, get_map_max_x, get_map_max_y,
    get_map_width, get_map_height, should_reset_losable_gold, get_shop,
    get_random_encounter
)

class MapZoneTests(TestCase):
    def setUp(self):
        self.original_zones = list(MAP_ZONES)

    def tearDown(self):
        MAP_ZONES.clear()
        MAP_ZONES.extend(self.original_zones)

    def test_map_zone_defines_space_and_offsets(self):
        grid = [
            "R^ ",
            " S."
        ]
        zone = MapZone(grid=grid, offset_x=5, offset_y=10)
        self.assertEqual(zone.width, 3)
        self.assertEqual(zone.height, 2)

        # Inside zone, non-space
        self.assertTrue(zone.defines_space(5, 10))  # 'R'
        self.assertTrue(zone.defines_space(6, 10))  # '^'
        self.assertFalse(zone.defines_space(7, 10)) # ' ' (space char)

        # Out of bounds
        self.assertFalse(zone.defines_space(4, 10))
        self.assertFalse(zone.defines_space(5, 9))
        self.assertFalse(zone.defines_space(8, 10))

    def test_negative_offsets_and_dynamic_bounds(self):
        grid1 = ["^^^", "^^^"] # 3x2 at (0, 0)
        grid2 = ["...", "..."] # 3x2 at (-5, -4)
        zone1 = MapZone(grid=grid1, offset_x=0, offset_y=0)
        zone2 = MapZone(grid=grid2, offset_x=-5, offset_y=-4)

        MAP_ZONES.clear()
        MAP_ZONES.extend([zone1, zone2])

        self.assertEqual(get_map_min_x(), -5)
        self.assertEqual(get_map_max_x(), 3)
        self.assertEqual(get_map_min_y(), -4)
        self.assertEqual(get_map_max_y(), 2)
        self.assertEqual(get_map_width(), 8)
        self.assertEqual(get_map_height(), 6)

        self.assertTrue(zone2.defines_space(-5, -4))
        self.assertEqual(get_tile(-5, -4), '.')
        self.assertEqual(get_tile(0, 0), '^')

    def test_overlapping_zones_priority_and_empty_space_fallthrough(self):
        # Zone 1 at (0, 0) has ' ' at (1, 0)
        grid1 = [
            "^ .",
            "..."
        ]
        # Zone 2 at (0, 0) has 'R' at (1, 0) and '_' at (0, 0)
        grid2 = [
            "_R_",
            "___"
        ]
        zone1 = MapZone(grid=grid1, offset_x=0, offset_y=0)
        zone2 = MapZone(grid=grid2, offset_x=0, offset_y=0)

        MAP_ZONES.clear()
        MAP_ZONES.extend([zone1, zone2])

        # At (0, 0), Zone 1 defines '^', taking priority over Zone 2's '_'
        self.assertEqual(get_tile(0, 0), '^')

        # At (1, 0), Zone 1 has ' ', so it falls through to Zone 2's 'R'
        self.assertEqual(get_tile(1, 0), 'R')

    def test_zone_getters_and_tile_descriptions(self):
        shop_data = [{'title': 'Custom Shop', 'items': [('Potion', 5)]}]
        inn_data = [{'id': 'custom_inn_1', 'title': 'Custom Inn'}]
        tile_descs = {'X': ('Custom Tile', 'A test tile.')}
        grid = [
            "XSI"
        ]
        zone = MapZone(
            grid=grid,
            offset_x=10,
            offset_y=20,
            shop_data=shop_data,
            inn_data=inn_data,
            tile_descriptions=tile_descs
        )

        MAP_ZONES.clear()
        MAP_ZONES.append(zone)

        self.assertEqual(get_tile(10, 20), 'X')
        self.assertEqual(get_tile_description(10, 20), ('Custom Tile', 'A test tile.'))

        shop = get_shop(11, 20)
        self.assertIsNotNone(shop)
        self.assertEqual(shop['title'], 'Custom Shop')

        inn = get_inn(12, 20)
        self.assertIsNotNone(inn)
        self.assertEqual(inn['id'], 'custom_inn_1')

        self.assertEqual(get_inn_id(12, 20), 'custom_inn_1')
        self.assertEqual(get_inn_coords('custom_inn_1'), (12, 20))
        self.assertEqual(get_nearest_inn_id(10, 20), 'custom_inn_1')


from game.quests import QUESTS, check_quest_triggers

class QuestTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_voinara_quest_proc_immediately(self):
        """Verify Voinara intro quest procs immediately on game start without requirements."""
        state = create_initial_game_state()
        self.assertEqual(state['screen'], 'dialog')
        self.assertIsNotNone(state.get('active_dialogue'))
        self.assertEqual(state['active_dialogue']['quest_id'], 'voinara_intro')
        self.assertEqual(state['active_dialogue']['step'], 0)

    def test_badgy_errand_step_0_proc_at_badgy_shop(self):
        """Test step 0 of Badgy's quest procs when visiting Badgy's General Store."""
        session = self.client.session
        state = create_initial_game_state()
        # Complete voinara intro
        state['quests']['voinara_intro'] = 1
        state['active_dialogue'] = None
        state['screen'] = 'overworld'

        # Find Badgy's shop location
        party = Party.from_dict(state['party'])
        badgy_x, badgy_y = None, None
        for zone in MAP_ZONES:
            for ly in range(len(zone.grid)):
                for lx in range(len(zone.grid[ly])):
                    if zone.grid[ly][lx] == 'S':
                        gx = lx + zone.offset_x
                        gy = ly + zone.offset_y
                        shop = zone.get_shop(gx, gy)
                        if shop and shop.get('title') == "Badgy's General Store":
                            badgy_x, badgy_y = gx, gy
                            break

        self.assertIsNotNone(badgy_x, "Badgy's General Store coordinates should be found on map")
        party.x, party.y = badgy_x, badgy_y
        check_quest_triggers(state, party)
        state['party'] = party.to_dict()
        session['game_state'] = state
        session.save()

        # Visit index
        response = self.client.get(reverse('game_index'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['screen'], 'dialog')
        self.assertEqual(response.context['title'], "Badgy's General Store")
        self.assertIn("Badgy", response.context['speaker'])
        self.assertEqual(len(response.context['responses']), 2)
        self.assertIn("I'd love to help", response.context['responses'][0])
        self.assertIn("Fine", response.context['responses'][1])

        # Advance dialogue
        post_response = self.client.post(reverse('handle_action'), {'action_type': 'dialog_advance'})
        self.assertEqual(post_response.status_code, 302)

        updated_state = self.client.session['game_state']
        self.assertEqual(updated_state['quests']['badgys_errand'], 1)

    def test_badgy_errand_step_1_card_consumption_and_rewards(self):
        """Test step 1 of Badgy's quest requires Rotten Egg, consumes it, and grants gold + card reward."""
        session = self.client.session
        state = create_initial_game_state()
        state['quests']['voinara_intro'] = 1
        state['quests']['badgys_errand'] = 1
        state['active_dialogue'] = None
        state['screen'] = 'overworld'

        # Find Badgy's shop location
        party = Party.from_dict(state['party'])
        for zone in MAP_ZONES:
            for ly in range(len(zone.grid)):
                for lx in range(len(zone.grid[ly])):
                    if zone.grid[ly][lx] == 'S':
                        gx = lx + zone.offset_x
                        gy = ly + zone.offset_y
                        shop = zone.get_shop(gx, gy)
                        if shop and shop.get('title') == "Badgy's General Store":
                            party.x, party.y = gx, gy

        # Without Rotten Egg, trigger returns False
        state['party'] = party.to_dict()
        self.assertFalse(check_quest_triggers(state, party))

        # Add Rotten Egg to inventory
        party.inventory.append('Rotten Egg')
        initial_gold = party.gold
        state['party'] = party.to_dict()

        # Trigger quest check
        triggered = check_quest_triggers(state, party)
        self.assertTrue(triggered)
        self.assertNotIn('Rotten Egg', party.inventory)
        self.assertIn('Honed Slash', party.inventory)
        self.assertEqual(party.gold, initial_gold + 50)
        self.assertEqual(state['screen'], 'dialog')
        self.assertEqual(state['active_dialogue']['quest_id'], 'badgys_errand')
        self.assertEqual(state['active_dialogue']['step'], 1)

    def test_title_and_illust_fallback_hierarchy(self):
        """Test title and illustration resolution hierarchy for dialog screen."""
        from game.quests import QUESTS
        session = self.client.session
        state = create_initial_game_state()
        party = Party.from_dict(state['party'])
        # Move party away from any inn/shop to open field
        party.x = 0
        party.y = 0
        state['party'] = party.to_dict()
        state['screen'] = 'dialog'
        
        # Inject custom step without title override to test fallback hierarchy
        test_quest_id = 'test_fallback_quest'
        QUESTS[test_quest_id] = {
            'id': test_quest_id,
            'title': 'Test Fallback Quest',
            'steps': [{
                'location': None,
                'dialogue': [{'speaker': 'Tester', 'text': 'Testing fallback', 'responses': ['...']}]
            }]
        }
        state['active_dialogue'] = {
            'quest_id': test_quest_id,
            'step': 0,
            'dialogue_index': 0
        }
        session['game_state'] = state
        session.save()

        response = self.client.get(reverse('game_index'))
        self.assertEqual(response.status_code, 200)
        # Should fallback to map tile location description for title since no shop/inn or entry override
        self.assertTrue(response.context['title'].startswith("Location:"))

        # Clean up temporary quest
        del QUESTS[test_quest_id]

    def test_get_active_quests_filtering_and_illustration(self):
        """Test get_active_quests filters out steps without menu_description and resolves card illust."""
        from game.quests import get_active_quests
        state = create_initial_game_state()
        state['quests']['voinara_intro'] = 1  # Completed voinara intro
        state['quests']['badgys_errand'] = 0   # At step 0 of badgy errand (has menu_description & Rotten Egg illust)

        active = get_active_quests(state)
        self.assertEqual(len(active), 1)
        quest_item = active[0]
        self.assertEqual(quest_item['id'], 'badgys_errand')
        self.assertEqual(quest_item['title'], "Badgy's Favor")
        self.assertIn("Rotten Egg", quest_item['description'])
        self.assertIn("(___)", quest_item['illust'])  # Rotten Egg ASCII art contains (___)

    def test_open_quest_menu_action_and_rendering(self):
        """Test toggling quest menu screen via action and rendering quest menu UI."""
        session = self.client.session
        state = create_initial_game_state()
        state['screen'] = 'overworld'
        state['quests']['voinara_intro'] = 1
        state['quests']['badgys_errand'] = 0
        session['game_state'] = state
        session.save()

        # Open quest menu
        response = self.client.post(reverse('handle_action'), {'action_type': 'open_quest_menu'})
        self.assertEqual(response.status_code, 302)

        # GET game index
        index_resp = self.client.get(reverse('game_index'))
        self.assertEqual(index_resp.status_code, 200)
        self.assertEqual(index_resp.context['screen'], 'quest_menu')
        self.assertIn('active_quests', index_resp.context)
        self.assertContains(index_resp, "+-+")
        self.assertContains(index_resp, "Badgy&#x27;s Favor")
        self.assertContains(index_resp, "y-scrollable")

        # Close quest menu
        close_resp = self.client.post(reverse('handle_action'), {'action_type': 'close_menu'})
        self.assertEqual(close_resp.status_code, 302)
        updated_state = self.client.session['game_state']
        self.assertEqual(updated_state['screen'], 'overworld')






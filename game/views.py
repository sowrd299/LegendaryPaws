import random
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .engine import (
    create_initial_game_state, Party, Character, CombatEngine,
    CARD_DATA, CARDS, CORE_STATS, DECK_MINIMUM_SIZE
)
from .map import WORLD_MAP, MAP_WIDTH, MAP_HEIGHT, TILE_DESCRIPTIONS, get_shop, get_random_encounter

VOINARA_DIALOGUE = [
    "Oh!, oh no, somethings have gone very strange...",
    "...I, have I lost you? That would be bad, who would know where that would be be... Oh! I see someone. It is you? It is Yew it seems. Where are they? " +
    "This little lost traveler has found themself somewhere very strange. I think you are about to witness quite the adventure.",
    "Something seems.... rotten, I think, in this place. It sounds like the locals call it the \"Death Rot\" whatever it is... " +
    "I just can't tell what it is that is rotting in the first place.",
    "Make good decisions please, this little traveler's future depends on it. Tell me what Yew finds... wherever this is."
]

INVENTORY_MAX_SIZE = 20

DEAD_ILLUST = """
    _____    
   /  (  \   
  | *   . |  
  |    .  |  
  |       |  
  |       |" 
-"~----~~-~-
"""

def name_to_card(card_name):
    card = dict(CARDS[card_name])
    return card

def list_to_unique_counts(l):
    d = dict()
    for i in l:
        if i in d:
            d[i] += 1
        else:
            d[i] = 1
    return [(i, d[i]) for i in d]

def get_game_state(request):
    """Loads game state from session or initializes a new one."""
    if 'game_state' not in request.session:
        request.session['game_state'] = create_initial_game_state()
        request.session.modified = True
    return request.session['game_state']


def save_game_state(request, state):
    """Saves game state to session."""
    request.session['game_state'] = state
    request.session.modified = True


def game_index(request):
    """Renders main game screen based on current session state."""
    state = get_game_state(request)
    party = Party.from_dict(state['party'])
    screen = state.get('screen', 'voinara_intro')

    party_inventory_cards = [ (name_to_card(name), count) for name,count in list_to_unique_counts(party.inventory) ]
    party_inventory_cards.sort(key = lambda card : CARD_DATA.index(CARDS[card[0]['name']]))

    party_deck_cards = [ (name_to_card(name), count) for name,count in list_to_unique_counts(party.shared_deck) ]
    party_deck_cards.sort(key = lambda card : CARD_DATA.index(CARDS[card[0]['name']]))


    # Prepare context data
    context = {
        'state': state,
        'screen': screen,
        'party': party,
        'party_inventory_cards': party_inventory_cards,
        'party_inventory_len': len(party.inventory),
        'inventory_max_size': INVENTORY_MAX_SIZE,
        'party_deck_cards': party_deck_cards,
        'party_deck_len': len(party.shared_deck),
        'deck_minimum_size': DECK_MINIMUM_SIZE,
        'dead_illust': DEAD_ILLUST,
    }

    if screen == 'voinara_intro':
        step = state.get('voinara_step', 0)
        context['speaker'] = "Voinara"
        context['text'] = VOINARA_DIALOGUE[min(step, len(VOINARA_DIALOGUE) - 1)]
        context['voinara_is_last'] = (step >= len(VOINARA_DIALOGUE) - 1)

    elif screen == 'overworld':
        # Render ASCII Map viewport with player location highlighted as '*'
        x, y = party.x, party.y
        current_tile = WORLD_MAP[y][x]
        tile_info = TILE_DESCRIPTIONS.get(current_tile, ('Unknown', 'A mysterious land.'))

        map_lines = []
        for r_idx, row in enumerate(WORLD_MAP):
            line_chars = []
            for c_idx, cell in enumerate(row):
                if r_idx == y and c_idx == x:
                    line_chars.append('*')
                else:
                    line_chars.append(cell)
            map_lines.append(" ".join(line_chars))

        context['map_grid'] = map_lines
        context['tile_name'] = tile_info[0]
        context['tile_desc'] = tile_info[1]
        context['current_tile'] = current_tile

    elif screen == 'character_menu':
        char_idx = state.get('char_index', 0)
        if char_idx >= 0:
            selected_char = party.members[char_idx] if party.members else None
            context['char_index'] = char_idx
            context['selected_char'] = selected_char
            context['stats_tab'] = state.get('stats_tab', True)
            if selected_char:
                scaled_stats = selected_char.get_scaled_stats()
                stat_xps = selected_char.get_stat_xps()
                context['scaled_core_stats'] = [ (name, stat, stat_xps[name]) for name, stat in scaled_stats.items() if name in CORE_STATS ]
                context['scaled_class_stats'] = [ (name, stat, stat_xps[name]) for name, stat in scaled_stats.items() if name not in CORE_STATS ]
                context['known_cards'] = [ name_to_card(name) for name in selected_char.get_known_cards() ]

    elif screen == 'shop':
        shop_data = get_shop(party.x, party.y)
        speaker, dialogue = random.choice(shop_data.get('dialogues', [("","")]))
        context['title'] = shop_data.get('title', '')
        context['illust'] = shop_data.get('illust', '')
        context['speaker'] = speaker
        context['text'] = dialogue
        context['shop_items'] = [(name_to_card(name), cost) for name,cost in shop_data.get('items', dict())]

    elif screen == 'combat':
        combat_dict = state.get('combat')
        if combat_dict:
            engine = CombatEngine.from_dict(combat_dict)
            turn_char = engine.advance_turn_timers()
            context['combat_engine'] = engine
            context['combat_engine_hand_cards'] = [ name_to_card(name) for name in ['Wait'] + engine.hand ]
            context['turn_char'] = turn_char
            context['is_player_turn'] = (turn_char in engine.allies) if turn_char else False

    return render(request, 'game/game.html', context)


def handle_action(request):
    """POST request endpoint for single-request user actions."""
    if request.method != 'POST':
        return redirect('game_index')

    state = get_game_state(request)
    party = Party.from_dict(state['party'])
    action_type = request.POST.get('action_type')

    if action_type == 'voinara_advance':
        step = state.get('voinara_step', 0) + 1
        if step >= len(VOINARA_DIALOGUE):
            state['screen'] = 'overworld'
            state['message'] = "You look upon the strange lands Voinara spoke of."
        else:
            state['voinara_step'] = step

    elif action_type == 'move':
        direction = request.POST.get('direction')
        new_x, new_y = party.x, party.y

        if direction == 'up' and party.y > 0:
            new_y -= 1
        elif direction == 'down' and party.y < MAP_HEIGHT - 1:
            new_y += 1
        elif direction == 'left' and party.x > 0:
            new_x -= 1
        elif direction == 'right' and party.x < MAP_WIDTH - 1:
            new_x += 1

        party.x, party.y = new_x, new_y
        current_tile = WORLD_MAP[new_y][new_x]

        # Check tile interaction / encounter
        if current_tile == 'S':
            state['screen'] = 'shop'
            state['message'] = "You enter the roadside shop."
        elif current_tile == 'I':
            # Inn auto heals party
            for m in party.members:
                m.current_hp = m.max_hp
            state['screen'] = 'inn'
            state['message'] = "You rest at the inn. Party HP fully restored!"
        else:
            # Chance for wild combat encounter based on terrain
            enemies = get_random_encounter(new_x, new_y, level=party.members[0].level if party.members else 1)
            if enemies:
                engine = CombatEngine(party.members, enemies, party.shared_deck)
                state['combat'] = engine.to_dict()
                state['screen'] = 'combat'
                state['message'] = f"Encountered wild enemy forces on the {TILE_DESCRIPTIONS.get(current_tile, ('tile', ''))[0]}!"
            else:
                state['message'] = f"Traveled to {TILE_DESCRIPTIONS.get(current_tile, ('tile', ''))[0]}."

    elif action_type == 'open_menu':
        if state['screen'] in ['overworld', 'shop', 'inn']:
            state['screen'] = 'character_menu'
            state['char_index'] = 0
            state['stat_tab'] = True

    elif action_type == 'close_menu':
        if state['screen'] in ['character_menu', 'shop', 'inn']:
            state['screen'] = 'overworld'

    elif action_type == 'select_char':
        idx = int(request.POST.get('char_index', 0))
        if 0 <= idx < len(party.members):
            state['char_index'] = idx

    elif action_type == 'select_deck':
        state['char_index'] = -1

    elif action_type == 'select_stats_tab':
        state['stats_tab'] = True

    elif action_type == 'select_card_tab':
        state['stats_tab'] = False

    elif action_type == 'give_card':
        card_name = request.POST.get('card_name')
        char_idx = state.get('char_index', 0)
        if char_idx < len(party.members) and card_name in party.inventory:
            char = party.members[char_idx]
            success, msg = char.give_card(card_name)
            if success:
                party.inventory.remove(card_name)
            state['message'] = msg

    elif action_type == 'remove_deck':
        card_name = request.POST.get('card_name')
        if card_name in party.shared_deck:
            party.shared_deck.remove(card_name)
            party.inventory.append(card_name)
            state['message'] = f"Removed {card_name} from your party's deck."

    elif action_type == 'add_deck':
        card_name = request.POST.get('card_name')
        if card_name in party.inventory:
            party.inventory.remove(card_name)
            party.shared_deck.append(card_name)
            state['message'] = f"Added {card_name} to your party's deck."

    elif action_type == 'shop_buy':
        card_name = request.POST.get('card_name')
        cost = int(request.POST.get('cost', 10))
        if party.gold >= cost and len(party.inventory) < INVENTORY_MAX_SIZE:
            party.gold -= cost
            party.inventory.append(card_name)
            state['message'] = f"Purchased {card_name} for {cost} gold!"
        else:
            state['message'] = "Not enough gold or inventory full!"

    elif action_type == 'combat_action':
        # Two-phase combat action: card_name + target_id in one request
        combat_dict = state.get('combat')
        if combat_dict:
            engine = CombatEngine.from_dict(combat_dict)
            card_name = request.POST.get('card_name', 'Slash')
            target_id = request.POST.get('target_id')

            turn_char = engine.get_current_turn_character()
            if turn_char and turn_char in engine.allies:
                engine.execute_player_turn(turn_char, card_name, target_id)

                # Do this here, where we have direct access to the game state
                if CARDS[card_name].get("is_consumable", False):
                    if card_name in party.inventory:
                        party.inventory.remove(card_name)
                    else:
                        party.shared_deck.remove(card_name)

                        if card_name in engine.discard_pile:
                            engine.discard_pile.remove(card_name)

                engine.check_combat_end()

                # Process subsequent enemy turns automatically until player turn or combat end
                while not engine.is_over:
                    next_char = engine.advance_turn_timers()
                    if not next_char:
                        break
                    if next_char in engine.enemies:
                        engine.execute_enemy_turn(next_char)
                        engine.check_combat_end()
                    else:
                        break  # It's player turn again!
                
                state['combat'] = engine.to_dict()

    elif action_type == "combat_end":
        combat_dict = state.get('combat')
        if combat_dict:
            engine = CombatEngine.from_dict(combat_dict)
            if engine.is_over:
                if engine.victory:
                    earned_gold = random.randint(5, 10)
                    party.gold += earned_gold
                    reward_card = random.choice(['Slash', 'Light Slash', 'First Aid', 'Wax', 'Wain', 'Pull of Tides', 'Singe', 'Singe Breath', 'Chill', 'Chill Breath'])

                    if len(party.inventory) < INVENTORY_MAX_SIZE:
                        party.inventory.append(reward_card)

                    # Copy character's HP stat out of combat, since the combat engine is a shallow copy
                    for m in party.members:
                        for a in engine.allies:
                            if a.id == m.id:
                                m.current_hp = a.current_hp

                    state['screen'] = 'overworld'
                    state['message'] = f"Victory! Gained {earned_gold} gold and a '{reward_card}' card!"
                else:
                    # Fully restore party on defeat & return to safe town position
                    for m in party.members:
                        m.current_hp = m.max_hp
                    party.x, party.y = 7, 5
                    state['screen'] = 'overworld'
                    state['message'] = "The Rot has overwhelmed your party! You safely retreated to town."

    state['party'] = party.to_dict()
    save_game_state(request, state)
    return redirect('game_index')


def reset_session(request):
    """Hidden debug view to reset the user's session and clear game progress."""
    request.session.flush()
    return render(request, 'game/reset.html', {
        'message': 'Debug mode: Game session has been reset successfully.'
    })


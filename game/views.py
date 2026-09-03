import random
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .engine import (
    create_initial_game_state, Party, Character, CombatEngine, Message,
    CORE_STATS, DECK_MINIMUM_SIZE, CLASS_DATA
)
from .cards import *
from .map import (
    get_tile, get_tile_description, get_map_width, get_map_height,
    get_map_min_x, get_map_min_y, get_map_max_x, get_map_max_y,
    VIEWPORT_MAX_WIDTH, VIEWPORT_MAX_HEIGHT, calculate_map_pan,
    should_reset_losable_gold, get_shop, get_inn, get_inn_id, get_inn_coords,
    get_nearest_inn_id, get_random_encounter, DEFAULT_START_INN_ID
)

from .quests import QUESTS, check_quest_triggers, get_active_quests

DEBUG_COMBAT_ENABLED = True

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

SIGNED_SCROLL_ILLUST = """

(=========(@  
 | ~~ ~~~~ | 
 | ~~~~ ~~ | 
 |  X_____ | 
(=========(@  
"""

INN_SIGN_ILLUST = """
  ==)===)===
    O   O
   ()  ()
  /-n---n-\ 
  |  INN  | 
  |  ===  / 
  +------/  
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


def advance_enemy_turns(engine):
    """Process subsequent enemy turns automatically until player turn or combat end"""

    while not engine.is_over:
        next_char = engine.advance_action_timers()
        if not next_char:
            break
        if next_char in engine.enemies:
            engine.execute_enemy_turn(next_char)
            engine.check_combat_end()
        else:
            break  # It's player turn again!


def game_index(request):
    """Renders main game screen based on current session state."""
    state = get_game_state(request)
    party = Party.from_dict(state['party'])
    log = [Message.from_dict(d) for d in state['log']]

    if len(log) > 15:
        log = log[-15:]

    screen = state.get('screen', 'dialog')

    party_inventory_cards = [ (name_to_card(name), count) for name,count in list_to_unique_counts(party.inventory) ]
    party_inventory_cards.sort(key = lambda card : CARD_DATA.index(CARDS[card[0]['name']]))

    party_deck_cards = [ (name_to_card(name), count) for name,count in list_to_unique_counts(party.shared_deck) ]
    party_deck_cards.sort(key = lambda card : CARD_DATA.index(CARDS[card[0]['name']]))


    # Prepare context data
    context = {
        'state': state,
        'screen': screen,
        'party': party,
        'log': log,
        'party_inventory_cards': party_inventory_cards,
        'party_inventory_len': len(party.inventory),
        'inventory_max_size': INVENTORY_MAX_SIZE,
        'party_deck_cards': party_deck_cards,
        'party_deck_len': len(party.shared_deck),
        'deck_minimum_size': DECK_MINIMUM_SIZE,
        'dead_illust': DEAD_ILLUST,
        'signed_scroll_illust': SIGNED_SCROLL_ILLUST,
        'inn_sign_illust': INN_SIGN_ILLUST,
        'party_len': len(party.members),
        'max_party_size': 4,
    }

    if screen == 'dialog':
        active_dialogue = state.get('active_dialogue')
        if active_dialogue:
            quest_id = active_dialogue.get('quest_id')
            step_idx = active_dialogue.get('step', 0)
            dialogue_idx = active_dialogue.get('dialogue_index', 0)

            quest = QUESTS.get(quest_id, {})
            steps = quest.get('steps', [])
            if step_idx < len(steps):
                step_data = steps[step_idx]
                dialogue_list = step_data.get('dialogue', [])
                if dialogue_idx < len(dialogue_list):
                    entry = dialogue_list[dialogue_idx]
                    speaker = entry.get('speaker', '')
                    text = entry.get('text', '')
                    responses = entry.get('responses', ['...'])

                    # Title resolution hierarchy
                    title = entry.get('title') or step_data.get('title')
                    shop_data = get_shop(party.x, party.y)
                    inn_data = get_inn(party.x, party.y)
                    if not title:
                        if shop_data:
                            title = shop_data.get('title')
                        elif inn_data:
                            title = inn_data.get('title')
                        else:
                            tile_info = get_tile_description(party.x, party.y)
                            title = f"Location: {tile_info[0]}"

                    # Illustration resolution hierarchy
                    illust = entry.get('illust') or step_data.get('illust')
                    if not illust:
                        if shop_data:
                            illust = shop_data.get('illust', '')
                        elif inn_data:
                            illust = inn_data.get('illust', '')
                        else:
                            illust = ''

                    context['speaker'] = speaker
                    context['text'] = text
                    context['title'] = title
                    context['illust'] = illust
                    context['responses'] = responses
                    context['dialogue_is_last'] = (dialogue_idx >= len(dialogue_list) - 1)

    elif screen == 'overworld':
        # Render ASCII Map viewport with player location highlighted as '*'
        x, y = party.x, party.y
        current_tile = get_tile(x, y)
        tile_info = get_tile_description(x, y)

        pan_x, pan_y = calculate_map_pan(x, y, state.get('pan_x'), state.get('pan_y'))
        state['pan_x'] = pan_x
        state['pan_y'] = pan_y
        save_game_state(request, state)

        vw = min(VIEWPORT_MAX_WIDTH, get_map_width())
        vh = min(VIEWPORT_MAX_HEIGHT, get_map_height())

        map_lines = []
        for r_idx in range(pan_y, pan_y + vh):
            line_chars = []
            for c_idx in range(pan_x, pan_x + vw):
                if r_idx == y and c_idx == x:
                    line_chars.append('*')
                else:
                    line_chars.append(get_tile(c_idx, r_idx))
            map_lines.append(line_chars)

        context['map_grid'] = map_lines
        context['tile_name'] = tile_info[0]
        context['tile_desc'] = tile_info[1]
        context['current_tile'] = current_tile

    elif screen == 'quest_menu':
        context['active_quests'] = get_active_quests(state)

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
                context['class_cards'] = [ name_to_card(name) for name in CLASS_DATA.get(selected_char.current_class, {}).get('default_cards', []) ]
                context['equipped_cards'] = [ name_to_card(name) for name in selected_char.equipped_cards ]

    elif screen == 'shop':
        shop_data = get_shop(party.x, party.y)
        if shop_data:
            speaker, dialogue = random.choice(shop_data.get('dialogues', [("","")]))
            context['title'] = shop_data.get('title', '')
            context['illust'] = shop_data.get('illust', '')
            context['speaker'] = speaker
            context['text'] = dialogue
            context['shop_items'] = [(name_to_card(name), cost) for name,cost in shop_data.get('items', dict())]

    elif screen == 'inn':
        inn_id = state.get('current_inn_id') or get_inn_id(party.x, party.y) or 'inn_0'
        inn_data = get_inn(party.x, party.y)
        if not inn_data:
            inn_data = {
                'title': 'The Inn',
                'illust': INN_SIGN_ILLUST,
                'dialogues': [("Innkeeper", "Welcome to the Inn!")]
            }
        speaker, dialogue = random.choice(inn_data.get('dialogues', [("Innkeeper", "Welcome to the Inn!")]))
        
        inns_dict = state.setdefault('inns', {})
        char_dicts = inns_dict.get(inn_id, [])
        inn_characters = [Character.from_dict(cd) for cd in char_dicts]

        context['title'] = inn_data.get('title', 'The Inn')
        context['illust'] = inn_data.get('illust', INN_SIGN_ILLUST)
        context['speaker'] = speaker
        context['text'] = dialogue
        context['inn_id'] = inn_id
        context['inn_characters'] = inn_characters

    elif screen == 'combat':
        combat_dict = state.get('combat')
        if combat_dict:
            engine = CombatEngine.from_dict(combat_dict)
            turn_char = engine.advance_action_timers()
            context['combat_engine'] = engine
            context['combat_engine_hand_cards'] = [ name_to_card(name) for name in ['Wait'] + engine.hand ]
            context['turn_char'] = turn_char
            context['is_player_turn'] = (turn_char in engine.allies) if turn_char else False
            context['log'] += engine.combat_log

            # Turn tracking UI data
            actual_living = engine.get_sorted_living_characters()
            actual_turns = []
            for c in actual_living:
                actual_turns.append({
                    'char': c,
                    'is_current': (c.id == turn_char.id if turn_char else False),
                    'is_enemy': (c in engine.enemies),
                    'action_timer': c.action_timer,
                })
            context['actual_turns'] = actual_turns

            hypothetical_turns = []
            if context['is_player_turn'] and turn_char:
                hand_card_names = ['Wait'] + engine.hand
                seen_cards = set()
                for card_name in hand_card_names:
                    if card_name in seen_cards:
                        continue
                    seen_cards.add(card_name)
                    hyp_info = engine.get_hypothetical_turn_info(card_name)
                    if hyp_info:
                        card_slug = card_name.replace(' ', '-').replace("'", "")
                        hypothetical_turns.append({
                            'card_name': card_name,
                            'card_slug': card_slug,
                            'target_index': hyp_info['target_index'],
                            'projected_timer': hyp_info['projected_timer'],
                            'char': turn_char,
                            'is_enemy': (turn_char in engine.enemies),
                        })
            context['hypothetical_turns'] = hypothetical_turns


    return render(request, 'game/game.html', context)


def handle_action(request):
    """POST request endpoint for single-request user actions."""
    if request.method != 'POST':
        return redirect('game_index')

    state = get_game_state(request)
    party = Party.from_dict(state['party'])
    log = [Message.from_dict(d) for d in state['log']]
    action_type = request.POST.get('action_type')

    if action_type == 'dialog_advance':
        active_dialogue = state.get('active_dialogue')
        if active_dialogue:
            quest_id = active_dialogue.get('quest_id')
            step_idx = active_dialogue.get('step', 0)
            dialogue_idx = active_dialogue.get('dialogue_index', 0)

            quest = QUESTS.get(quest_id, {})
            steps = quest.get('steps', [])
            if step_idx < len(steps):
                step_data = steps[step_idx]
                dialogue_list = step_data.get('dialogue', [])
                next_idx = dialogue_idx + 1

                if next_idx < len(dialogue_list):
                    state['active_dialogue']['dialogue_index'] = next_idx
                else:
                    # Step completed!
                    if 'quests' not in state:
                        state['quests'] = {}

                    state['quests'][quest_id] = step_idx + 1
                    state['active_dialogue'] = None
                    state['screen'] = 'overworld'

                    completion_log = step_data.get('completion_log')
                    if completion_log:
                        log.append(Message(1, completion_log))

                    # Re-check quest triggers
                    check_quest_triggers(state, party)

    elif action_type == 'move':
        direction = request.POST.get('direction')
        new_x, new_y = party.x, party.y

        if direction == 'up' and party.y > get_map_min_y():
            new_y -= 1
        elif direction == 'down' and party.y < get_map_max_y() - 1:
            new_y += 1
        elif direction == 'left' and party.x > get_map_min_x():
            new_x -= 1
        elif direction == 'right' and party.x < get_map_max_x() - 1:
            new_x += 1

        prev_x, prev_y = party.x, party.y
        party.x, party.y = new_x, new_y
        current_tile = get_tile(new_x, new_y)

        if should_reset_losable_gold(new_x, new_y):
            party.losable_gold = 0
        
        tile_desc = get_tile_description(new_x, new_y)

        # Check tile interaction / encounter
        if not current_tile or current_tile == ' ': # nothingness
            party.x, party.y = prev_x, prev_y
        elif current_tile == '~': # water
            party.x, party.y = prev_x, prev_y
            log.append(Message(2, f"You look at {tile_desc[0]}, {tile_desc[1]}, <span style='color:var(--accent-red)'>but your party can't swim!</span>"))
        elif current_tile == 'S':
            state['screen'] = 'shop'
            log.append(Message(1, 'You enter a shop.'))
            check_quest_triggers(state, party)
        elif current_tile == 'I':
            # Inn auto heals party
            for m in party.members:
                m.current_hp = m.max_hp
            inn_id = get_inn_id(new_x, new_y) or DEFAULT_START_INN_ID
            state['current_inn_id'] = inn_id
            state['respawn_inn_id'] = inn_id
            state['screen'] = 'inn'
            log.append(Message(1, '<span style="color:var(--accent-green)">After resting at the inn, your party is fully healed!</span>'))
            check_quest_triggers(state, party)
        else:
            # Chance for wild combat encounter based on terrain
            enemies, is_recruitable, reward_card, reward_gold = get_random_encounter(new_x, new_y)
            if enemies and DEBUG_COMBAT_ENABLED:
                engine = CombatEngine(party.members, enemies, party.shared_deck, is_recruitable=is_recruitable, reward_card=reward_card, reward_gold=reward_gold)
                engine.start_combat()
                state['combat'] = engine.to_dict()
                state['screen'] = 'combat'
                if is_recruitable:
                    log.append(Message(1, f"Encountered another brigand on the {tile_desc[0]}; unsure if you can trust eachother, you draw weapons!"))
                else:
                    log.append(Message(1, f"The Rot descends upon your party on the {tile_desc[0]}!"))
            else:
                log.append(Message(-1, f"Traveled to {tile_desc[0]}."))
                check_quest_triggers(state, party)


    elif action_type == 'open_menu':
        if state['screen'] in ['overworld', 'quest_menu', 'shop', 'inn']:
            state['screen'] = 'character_menu'
            state['char_index'] = 0
            state['stat_tab'] = True

    elif action_type == 'open_quest_menu':
        if state['screen'] in ['overworld', 'shop', 'inn']:
            state['screen'] = 'quest_menu'
        elif state['screen'] == 'quest_menu':
            state['screen'] = 'overworld'

    elif action_type == 'close_menu':
        if state['screen'] in ['character_menu', 'quest_menu', 'shop', 'inn']:
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
            log.append(Message(0, msg))

    elif action_type == 'change_class':
        new_class = request.POST.get('class_name')
        if new_class in party.members[state.get('char_index', 0)].unlocked_classes:
            party.members[state.get('char_index', 0)].current_class = new_class
            log.append(Message(0, f"{party.members[state.get('char_index', 0)].name} is now practicing as a {new_class}."))

    elif action_type == 'remove_deck':
        card_name = request.POST.get('card_name')
        if card_name in party.shared_deck:
            party.shared_deck.remove(card_name)
            party.inventory.append(card_name)
            log.append(Message(0, f"Removed {card_name} from your party's deck."))

    elif action_type == 'add_deck':
        card_name = request.POST.get('card_name')
        if card_name in party.inventory:
            party.inventory.remove(card_name)
            party.shared_deck.append(card_name)
            log.append(Message(0, f"Added {card_name} to your party's deck."))

    elif action_type == 'shop_buy':
        card_name = request.POST.get('card_name')
        cost = int(request.POST.get('cost', 10))
        if party.gold < cost:
            log.append(Message(2, "<span style='color:var(--accent-red)'>You can't afford that!</span>"))
        elif len(party.inventory) >= INVENTORY_MAX_SIZE:
            log.append(Message(2, "<span style='color:var(--accent-red)'>Your inventory is full!</span>"))
        else:
            party.gold -= cost
            party.inventory.append(card_name)
            log.append(Message(1, f"Purchased {card_name} for {cost} gold!"))

    elif action_type == 'inn_recruit':
        inn_id = state.get('current_inn_id') or get_inn_id(party.x, party.y) or 'inn_0'
        inns_dict = state.setdefault('inns', {})
        inn_chars = inns_dict.get(inn_id, [])
        try:
            char_idx = int(request.POST.get('char_index', 0))
        except (ValueError, TypeError):
            char_idx = -1

        if len(party.members) >= 4:
            log.append(Message(2, "<span style='color:var(--accent-red)'>Your party is already full!</span>"))
        elif 0 <= char_idx < len(inn_chars):
            char_dict = inn_chars.pop(char_idx)
            recruited_char = Character.from_dict(char_dict)
            recruited_char.current_hp = recruited_char.max_hp
            party.members.append(recruited_char)
            log.append(Message(0, f"Recruited {recruited_char.name} into your party!"))

    elif action_type == 'inn_dismiss':
        inn_id = state.get('current_inn_id') or get_inn_id(party.x, party.y) or 'inn_0'
        inns_dict = state.setdefault('inns', {})
        try:
            char_idx = int(request.POST.get('char_index', 0))
        except (ValueError, TypeError):
            char_idx = -1

        if len(party.members) <= 1:
            log.append(Message(2, "<span style='color:var(--accent-red)'>You must keep at least one person in your party!</span>"))
        elif 0 <= char_idx < len(party.members):
            dismissed_char = party.members.pop(char_idx)
            dismissed_char.current_hp = dismissed_char.max_hp
            inns_dict.setdefault(inn_id, []).append(dismissed_char.to_dict())
            log.append(Message(0, f"Left {dismissed_char.name} resting at the Inn."))

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
                if not engine.is_over:
                    advance_enemy_turns(engine)

                state['combat'] = engine.to_dict()

    elif action_type == "advance_combat":
        combat_dict = state.get('combat')
        if combat_dict:
            engine = CombatEngine.from_dict(combat_dict)
            if not engine.is_over:
                advance_enemy_turns(engine)
                state['combat'] = engine.to_dict()

    elif action_type == "combat_end":
        combat_dict = state.get('combat')
        if combat_dict:
            engine = CombatEngine.from_dict(combat_dict)
            if engine.is_over:
                if engine.victory:
                    earned_gold = engine.reward_gold
                    party.gold += earned_gold
                    party.losable_gold += earned_gold
                    reward_card = engine.reward_card 

                    reward_string = f"Gained {earned_gold} gold, <span style='color:var(--accent-red)'>but your inventory is full.</span>"
                    if len(party.inventory) < INVENTORY_MAX_SIZE:
                        party.inventory.append(reward_card)
                        reward_string = f"Gained {earned_gold} gold and a '{reward_card}' card!"
                    else:
                        reward_card = None

                    # Copy character's HP stat out of combat, since the combat engine is a shallow copy
                    for m in party.members:
                        for a in engine.allies:
                            if a.id == m.id:
                                m.current_hp = a.current_hp

                    recruited_msgs = []
                    for e in engine.enemies:
                        if getattr(e, 'is_recruited', False):
                            e.current_hp = e.max_hp
                            e.is_recruited = False
                            e.status_effects = []
                            if len(party.members) < 4:
                                party.members.append(e)
                                recruited_msgs.append(f"Recruited {e.name} into your party!")
                            else:
                                nearest_inn_id = get_nearest_inn_id(party.x, party.y)
                                inns_dict = state.setdefault('inns', {})
                                inns_dict.setdefault(nearest_inn_id, []).append(e.to_dict())
                                recruited_msgs.append(f"{e.name} was recruited and sent to the nearest Inn ({nearest_inn_id})!")

                    recruited_str = (" " + " ".join(recruited_msgs)) if recruited_msgs else ""
                    state['screen'] = 'overworld'
                    log.append(Message(3,f"Victory! {reward_string}{recruited_str}", reward_card))
                    check_quest_triggers(state, party)
                else:
                    # Fully restore party on defeat & return to respawn Inn position
                    for m in party.members:
                        m.current_hp = m.max_hp
                    respawn_inn_id = state.get('respawn_inn_id') or DEFAULT_START_INN_ID
                    rx, ry = get_inn_coords(respawn_inn_id)
                    party.x, party.y = rx, ry
                    state['pan_x'], state['pan_y'] = calculate_map_pan(party.x, party.y)
                    state['screen'] = 'overworld'
                    log.append(Message(3, f"The Rot has overwhelmed your party! You fled back to the inn and lost {party.losable_gold} gold!"))
                    party.gold -= party.losable_gold
                    party.gold = max(party.gold, 0)
                    party.losable_gold = 0
                    check_quest_triggers(state, party)

                # Update character's previous combat class
                for m in party.members:
                    m.previous_combat_class = m.current_class

    state['party'] = party.to_dict()
    state['log'] = [m.to_dict() for m in log]
    save_game_state(request, state)
    return redirect('game_index')


def reset_session(request):
    """Hidden debug view to reset the user's session and clear game progress."""
    request.session.flush()
    return render(request, 'game/reset.html', {
        'message': 'Debug mode: Game session has been reset successfully.'
    })


"""
Quests data architecture and trigger evaluation for Legendary Paws.
"""

from .engine import Character
from .map import get_shop, get_inn, get_inn_id, get_nearest_inn_id, get_tile_description
from .cards import CARDS

VOINARA_ILLUST = """
+--------------------------------------------------------------------------------------------------+
|                                                 ___                                              |
|           *                                   // / \`                                            |
|                                     *        ((   / ))                    *                      |
|                                               `\   //                                            |
|                                                `\=//                                             |
|                                                 ) (                                              |
|                        *                        (&)                               *              |
|                                                            *                                     |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
"""

QUESTS = {
    'voinara_intro': {
        'id': 'voinara_intro',
        'title': 'Voinara\'s Biding',
        'steps': [
            {
                'location': None,  # Proc anywhere / immediately
                'reward_cards': [],
                'reward_gold': 0,
                'dialogue': [
                    {
                        'title': "<span style='color: var(--accent-amber)'>Wanderlust Pause</span>",
                        'illust': VOINARA_ILLUST,
                        'speaker': 'Voinara',
                        'text': 'Oh!, oh no, somethings have gone very strange...',
                        'responses': ['...']
                    },
                    {
                        'title': "<span style='color: var(--accent-amber)'>Wanderlust Pause</span>",
                        'illust': VOINARA_ILLUST,
                        'speaker': 'Voinara',
                        'text': '...I, have I lost you? That would be bad, who would know where that would be be... Oh! I see someone. It is you? It is Yew it seems. Where are they? '
                                'This little lost traveler has found themself somewhere very strange. I think you are about to witness quite the adventure.',
                        'responses': ['...']
                    },
                    {
                        'title': "<span style='color: var(--accent-amber)'>Wanderlust Pause</span>",
                        'illust': VOINARA_ILLUST,
                        'speaker': 'Voinara',
                        'text': 'Something seems.... rotten, I think, in this place. It sounds like the locals call it the "Death Rot" whatever it is... '
                                'I just can\'t tell what it is that is rotting in the first place.',
                        'responses': ['...']
                    },
                    {
                        'title': "<span style='color: var(--accent-amber)'>Wanderlust Pause</span>",
                        'illust': VOINARA_ILLUST,
                        'speaker': 'Voinara',
                        'text': 'Make good decisions please, this little traveler\'s future depends on it. Tell me what Yew finds... wherever this is.',
                        'responses': ['...']
                    }
                ],
                'completion_log': "You peer through Voinara's mirror, and see Yew standing on the Strange Lands she spoke of..."
            }, 
            {
                'location': None,
                'required_cards_have': ['Dragonsbane'],
                'menu_description': "Explore the Strange Lands, and investigate the Death Rot.",
                'reward_cards': [],
                'reward_gold': 0,
                'dialogue': [
                    {
                        'illust': VOINARA_ILLUST,
                        'speaker': 'Voinara',
                        'text': 'Oh, I see... it\'s almost like what\'s "rotting" here is Death itself... these poor people really should be long dead, they\'re just, not?',
                        'responses': [
                            'Ah, so you are still watching over me, old friend',
                            'Are you going to just leave here to deal with this by myself?',
                        ]
                    },
                    {
                        'illust': VOINARA_ILLUST,
                        'speaker': 'Voinara',
                        'text': 'Unfortunately, I think it\'s all up to Yew.',
                        'responses': [
                            '...',
                        ]
                    },
                ]

            }
        ]
    },
    'meet_conny': {
        'id': 'meet_conny',
        'title': 'Good Morning Conny!',
        'steps': [
            {
                'location': 'New Dunton Village',
                'reward_characters': [Character(species='Rabbit', current_class='Shieldmate', name='Conny')],
                'dialogue': [
                    {
                        'speaker': 'Conny',
                        'text': "Hello Yew! Rest well? What's the plan for today? Tredge off into the Rot for gold? glory? the Good of the Strange Lands? "
                                "getting to Yonder?",
                        'responses': [
                            'For Gold!',
                            'For Glory!',
                            'For the Good of the Strange Lands!',
                            'I don\'t think we\'re getting to Yonder today.'
                        ],
                    }
                ],
                'completion_log': "Conny rejoined Yew's party!"
            }
        ]
    },
    'badgys_errand': {
        'id': 'badgys_errand',
        'title': "Badgy's Favor",
        'steps': [
            {
                'location': "Badgy's General Store",
                'reward_cards': [],
                'reward_gold': 0,
                'dialogue': [
                    {
                        'speaker': 'Badgy',
                        'text': "Ah, hello brigand! You know, this Death Rot's strange stuff. "
                                "I've got a colleague over in Yonder who's busy collecting eggs infected with the stuff! "
                                "He says he has brigands like you paying hansomely for them, though you won't make much good of them without a friend to stuff them down your throught. "
                                "I hear there's some dragonling husks who've been hoarding these eggs in a field north of here. "
                                "If you find one, bring it to me and I'll see what I can get my colleague to pay for it.",
                        'responses': [
                            "I'd love to help you find a Rotten Egg!",
                            "Fine, if I come across one I'll bring it back..."
                        ]
                    }
                ],
                'completion_log': "Accepted Badgy's request to bring him a Rotten Egg from the wild."
            },
            {
                'location': "Badgy's General Store",
                'menu_description': "Get a rotten egg from the dragonling husks in the field north of New Dunton Village, and give it to Badgy in his store.",
                'menu_illust': 'Rotten Egg',
                'required_cards_give': ['Rotten Egg'],
                'reward_cards': ['Honed Slash'],
                'reward_gold': 50,
                'dialogue': [
                    {
                        'speaker': 'Badgy',
                        'text': "Ah! Is that a Rotten Egg you have there? Brilliant!",
                        'responses': [
                            "Always happy to help!",
                            "Here's your gross egg. Now give me the gold."
                        ]
                    }
                ],
                'completion_log': "Delivered the Rotten Egg to Badgy! Received 50 gold and a Honed Slash card."
            }
        ]
    }
}


def is_location_match(req_loc, party_x, party_y):
    """Checks if party's current location satisfies req_loc (inn_id, shop_title, or None)."""
    if req_loc is None:
        return True

    # Check shop
    shop = get_shop(party_x, party_y)
    if shop and shop.get('title') == req_loc:
        return True

    # Check inn
    inn = get_inn(party_x, party_y)
    if inn:
        if inn.get('id') == req_loc or inn.get('title') == req_loc:
            return True

    # Check tile description
    tile_desc = get_tile_description(party_x, party_y)
    if tile_desc and tile_desc[0] == req_loc:
        return True

    return False


def has_required_cards(required_cards, inventory):
    """Checks if inventory contains all required_cards."""
    if not required_cards:
        return True

    inv_copy = list(inventory)
    for card in required_cards:
        if card in inv_copy:
            inv_copy.remove(card)
        else:
            return False
    return True


def check_quest_triggers(state, party):
    """Evaluates all quests in state and triggers dialogue screen if conditions for a step are met."""
    if state.get('screen') == 'dialog' or state.get('active_dialogue'):
        return False

    if state.get('screen') in ['combat', 'character_menu']:
        return False

    quests_progress = state.get('quests', {})

    for quest_id, quest_data in QUESTS.items():
        current_step_idx = quests_progress.get(quest_id, 0)
        steps = quest_data.get('steps', [])

        if current_step_idx < len(steps):
            step_data = steps[current_step_idx]
            req_loc = step_data.get('location')
            req_cards_have = step_data.get('required_cards_have', [])
            req_cards_give = step_data.get('required_cards_give', [])

            if is_location_match(req_loc, party.x, party.y) and has_required_cards(req_cards_have + req_cards_give, party.inventory):
                # Deduct required cards
                for card in req_cards_give:
                    if card in party.inventory:
                        party.inventory.remove(card)

                # Award gold
                reward_gold = step_data.get('reward_gold', 0)
                if reward_gold > 0:
                    party.gold += reward_gold

                # Award cards
                reward_cards = step_data.get('reward_cards', [])
                for card in reward_cards:
                    party.inventory.append(card)

                # Award characters
                reward_characters = step_data.get('reward_characters', [])
                for e in reward_characters:
                    if len(party.members) < 4:
                        party.members.append(e)
                    else:
                        nearest_inn_id = get_nearest_inn_id(party.x, party.y)
                        inns_dict = state.setdefault('inns', {})
                        inns_dict.setdefault(nearest_inn_id, []).append(e.to_dict())

                # Activate dialogue screen
                state['screen'] = 'dialog'
                state['active_dialogue'] = {
                    'quest_id': quest_id,
                    'step': current_step_idx,
                    'dialogue_index': 0
                }
                return True

    return False


def get_active_quests(state):
    """
    Returns a list of active quest dicts that have a menu_description for their current step.
    Each returned dict has:
    - 'id': quest_id
    - 'title': quest_title
    - 'description': menu_description
    - 'illust': ASCII illustration string (from CARDS[menu_illust] if referenced, or '')
    """
    quests_progress = state.get('quests', {})
    active = []

    for quest_id, quest_data in QUESTS.items():
        current_step_idx = quests_progress.get(quest_id, 0)
        steps = quest_data.get('steps', [])

        if current_step_idx < len(steps):
            step_data = steps[current_step_idx]
            menu_desc = step_data.get('menu_description') or step_data.get('description')

            if menu_desc:
                card_name = step_data.get('menu_illust') or step_data.get('illust_card') or step_data.get('card_name')
                illust_str = ''
                if card_name and card_name in CARDS:
                    illust_str = CARDS[card_name].get('illust', '')

                active.append({
                    'id': quest_id,
                    'title': quest_data.get('title', quest_id),
                    'description': menu_desc,
                    'illust': illust_str,
                })

    return active


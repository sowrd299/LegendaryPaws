"""
Quests data architecture and trigger evaluation for Legendary Paws.
"""

from .map import get_shop, get_inn, get_inn_id, get_tile_description

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
        'title': 'Voinara Intro',
        'steps': [
            {
                'location': None,  # Proc anywhere / immediately
                'required_cards': [],
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
            }
        ]
    },
    'badgys_errand': {
        'id': 'badgys_errand',
        'title': "Badgy's Errand",
        'steps': [
            {
                'location': "Badgy's General Store",
                'required_cards': [],
                'reward_cards': [],
                'reward_gold': 0,
                'dialogue': [
                    {
                        'speaker': 'Badgy',
                        'text': "Ah, hello brigand! You know, this Death Rot's strange stuff. "
                                "I've got college over in Yonder who's busy collecting eggs infected with the stuff! "
                                "He says he has brigands like you paying hansomely for them, though you won't make much good of them without a friend to stuff them down your throught. "
                                "I hear there's some dragonling husks who've been hoarding these eggs in a field north of here. "
                                "If you find one, bring it to me and I'll see what I can get my college to pay for it.",
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
                'required_cards': ['Rotten Egg'],
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
            req_cards = step_data.get('required_cards', [])

            if is_location_match(req_loc, party.x, party.y) and has_required_cards(req_cards, party.inventory):
                # Deduct required cards
                for card in req_cards:
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

                # Activate dialogue screen
                state['screen'] = 'dialog'
                state['active_dialogue'] = {
                    'quest_id': quest_id,
                    'step': current_step_idx,
                    'dialogue_index': 0
                }
                return True

    return False

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
                            'Are you going to just leave me here to deal with this by myself?',
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
    'library_donations': {
        'id': 'library_donations',
        'title': 'The Library\'s Collection',
        'steps': [
            {
                'location': 'Library',
                'reward_cards': [],
                'reward_gold': 0,
                'dialogue': [
                    {
                        'speaker': 'Librarian',
                        'text': "It's a shame the Strange Lands Library System isn't the premier piece of transport infrastructure it was before the Rot. "
                                "We can't have librarians running from library to library anymore, obviously, but we still pay "
                                "enough brigands to get the important bits from one library to the next. ",
                        'responses': [
                            "Can I help?",
                            "That's impressive for a library.",
                        ]
                    },
                    {
                        'speaker': 'Librarian',
                        'text': "Most of our old collection, however, was lost in the chaos that followed the Rot. I hope you'll benefit as much from helping us rebuild it as we will.",
                        'responses': [
                            "I'd love to help with the library!",
                            "Could I convince you to pay me?",
                            "Fine, if I wind up with spare findings I'll bring them back...",
                        ]
                    }
                ],
                'completion_log': "Accepted the library's request to donate books."
            },
            {
                'location': 'An imaginary place that doesn\'t exist, nah nah you\'ll never finish this quest',
                'menu_description': "Donate cards Yew finds on their journey to the Library to uncover lost texts.",
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
    },
    'hemlocks_errand': {
        'id': 'hemlocks_errand',
        'title': "Hemlock's Snipe Hunt",
        'steps': [
            {
                'location': "Hemlock\'s Miscellany",
                'reward_cards': [],
                'reward_gold': 0,
                'dialogue': [
                    {
                        'speaker': 'Hemlock',
                        'text': "You know, these eggs are turning into pretty great business. I wonder what I could do with a propper hunk of flesh off of one of those hollow "
                                "\"people\". It's pretty hard to get; usually their too decayed. I hear they're some tough specimens in the ruins south of here; maybe a hunk of "
                                "one of them will hold up well enough...",
                        'responses': [
                            "I'd love to help you find a hunk of pure Death Rot!",
                            "What exactly do you plan to do with that..."
                        ]
                    }
                ],
                'completion_log': "Accepted Hemlock's request to bring him Rot Remains from the ruins."
            },
            {
                'location': "Hemlock\'s Miscellany",
                'menu_description': "Get Rot Remains from the Rot in the ruins south of Yonder, and give it to Hemlock in his shop.",
                'menu_illust': 'Rot Remains',
                'required_cards_give': ['Rot Remains'],
                'reward_gold': 200,
                'dialogue': [
                    {
                        'speaker': 'Hemlock',
                        'text': "Heh, brilliant! Look at that... beautiful?... decay! It's so... gray? I'll figure out what to do with this now.",
                        'responses': [
                            "I look forward to your mercantile discoveries!",
                            "I carried that thing this far... and you're not even sure what it's for?",
                            "Is this at all safe?",
                        ]
                    },
                    {
                        'speaker': 'Hemlock',
                        'text': "Who knows what'll come of any of this rot? Anyways, know you, this town used to have a pretty excellent brigand defending us, "
                                "Imora her name was. She could evaporate Rot with her bow practically miles away. I'd love to see up us that that certainty again. "
                                "Mind seeing what you can find about being able to Snipe like her? Last I heard she was on patrol in the pondlands up north.",
                        'responses': [
                            "To the pondlands I go!",
                            "The Rot doesn't spare anyone, does it? I'll see what I can do.",
                            "How long after I set off did you realize you wanted this too?",
                        ]
                    },
                ],
                'completion_log': "Delivered the Rot Remains to Hemlock! Received 200 gold. Accepted Hemlock's request to bring him a Snipe."
            }, 
            {
                'location': "Hemlock\'s Miscellany",
                'menu_description': "Discover the technique of Imora's Snipe in the pondlands north of Yonder, and give it to Hemlock in his shop.",
                'menu_illust': 'Snipe',
                'required_cards_give': ['Snipe'],
                'reward_gold': 400,
                'dialogue': [
                    {
                        'speaker': 'Hemlock',
                        'text': "Look at that! I'll be defending Yonder like Imora used to in no time! Or maybe they're a few things to learn first. "
                                "It probably wouldn't hurt if I could set a trap to catch the Rot in first to snipe them in... and I'd probably need quite a bit of experience. "
                                "Or maybe the trick is to be a cat like Imora.",
                        'responses': [
                            "I'm sure you will!",
                            "Maybe I would have been better off keeping that for myself."
                        ]
                    },
                ],
                'completion_log': "Delivered the Snipe to Hemlock! Received 400 gold."
            },
        ]
    }, 
    'imoras_death': {
        'id': 'imoras_death',
        'title': "Imora's Death",
        'steps': [
            {
                'location': "Imora's Resting Place",
                'reward_cards': ['Assassinate', 'Snipe'],
                'reward_gold': 0,
                'dialogue': [
                    {
                        'speaker': 'Imora, Husk of a Cat Assassin',
                        'text': "I... oh... PAIN... such pain... everything,",
                        'responses': [
                            "Hello?",
                            "Imora?",
                            "...",
                        ]
                    },
                    {
                        'speaker': 'Imora, Husk of a Cat Assassin',
                        'text': "burns. so. cold...",
                        'responses': [
                            "Can I help?",
                            "...",
                        ]
                    },
                    {
                        'speaker': 'Imora, Husk of a Cat Assassin',
                        'text': "The giant's sword... lethal... but, no, no death... no White Beetle...",
                        'responses': [
                            "...",
                        ]
                    },
                    {
                        'speaker': 'Imora, Husk of a Cat Assassin',
                        'text': "Just... my mind, thinking, everything, burns cold with PAIN...",
                        'responses': [
                            "...",
                        ]
                    },
                    {
                        'speaker': 'Imora, Husk of a Cat Assassin',
                        'text': "Take...",
                        'responses': [
                            "Thank you.",
                            "I hope the pain ends.",
                            "...",
                        ]
                    },
                ],
                'completion_log': "As Imora succumbs to the Rot, she gifts you with her skills."
            }
        ]
    },
    'sallys_curiosity': {
        'id': 'sallys_curiosity',
        'title': "Sally's Curiosity",
        'steps': [
            {
                'location': "Sally's School Supplies",
                'dialogue': [
                    {
                        'speaker': 'Sally',
                        'text': "Hello there Brigand. Have you ever considered broadening your horizons? Becoming a whole new class of brigand? "
                                "It is my mission here to help wanderers like you learn to do just that.",
                        'responses': [
                            "You know, I've been considering studying Star Magic",
                            "I suppose I'll take a look",
                            "We are quite happy with the classes we fill, please and thank you",
                        ]
                    },
                    {
                        'speaker': 'Sally',
                        'text': "Even I don't know all the specialities you can learn of course, just the basics really. I've heard there are brigands "
                                "out there who wield a blend of Moon Magic and survival craft to totally desolve into the wilds. They call themselves \"Blackcloaks\" "
                                "I think. I'd love to meet one one day and chat about their craft. I imagine the spell Wax must be very important to them.",
                        'responses': [
                            "If I come across one I'll bring them your way",
                            "Sound like weirdos with nothing to contribute to my party",
                        ]
                    }
                ],
                'completion_log': "Accepted Sally's request to help her meet a Blackcloak."
            },
            {
                'menu_description': "Bring a Blackcloak to meet Sally at her shop in Yonder. Blackcloaks specialize in Moon Magic and survival craft. "
                                    "The card Wax might have a clue on how to become one.",
                'menu_illust': "Cover of Night",
                'location': "Sally's School Supplies",
                'required_classes': ['Blackcloak'],
                'reward_cards': ["New Moon"],
                'dialogue': [
                    {
                        'speaker': 'Sally',
                        'text': "Oh, a Blackcloak! Splendid, splendid! Do come in, do come in! I found this scroll that I was hoping a Blackcloak would like. Please, take it.",
                        'responses': [
                            "It was quite the adventure getting here",
                            "It was nothing",
                            "You sure have interesting curiosities",
                        ]
                    },
                    {
                        'speaker': 'Sally',
                        'text': "Well, I've got another favor if you're up for it. I was reading about \"fencers\". Apparently they have quite some unique techniques in combat "
                                "from what I've read the hard part of becoming one is getting an opportunity to learn the basic weapon at all. "
                                "Some of the books mention a \"flowering stab\". Most of the mentions I've heard of fencer come from the east, so maybe that's a good place to look.",
                        'responses': [
                            "If I come across one I'll bring them your way",
                            "Sound like more weirdos with nothing to contribute to my party",
                        ]
                    }
                ],
                'completion_log': "Sally met a Blackcloak. Received a New Moon card. Accepted Sally's request to help her meet a Fencer."
            },
            {
                'menu_description': "Bring a Fencer to meet Sally at her shop in Yonder. "
                                    "Apparently Fencers are common in the east, and the card Flowering Stab might have a clue on how to become one.",
                'menu_illust': "Flowering Stab",
                'location': "Sally's School Supplies",
                'required_classes': ['Fencer'],
                'reward_cards': ["Flowering Stab"],
                'dialogue': [
                    {
                        'speaker': 'Sally',
                        'text': "Oh, a Fencer! A joy to meet you! Do come in, do come in! I want to learn what you do. Maybe I can replicate it!",
                        'responses': [
                            "It was quite the adventure getting here",
                            "It was nothing",
                            "You sure have interesting curiosities",
                        ]
                    },
                    {
                        'speaker': 'Sally',
                        'text': "I do have a third favor if you're up for it. I was talking to Hemlock about a wizard me met. "
                                "I love the idea of a mage who stays devouted to well rounded study, even past their student days. "
                                "According to Hemlock, every wizard he's ever met is an owl. I'm not sure if there's a reason for that.",
                        'responses': [
                            "If I come across one I'll bring them your way",
                            "Seriously, they can't just specialize like a normal mage?",
                        ]
                    }
                ],
                'completion_log': "Sally met a Fencer. Received a Flowering Stab card. Accepted Sally's request to help her meet a Wizard."
            },
            {
                'menu_description': "Bring a Wizard to meet Sally at her shop in Yonder. "
                                    "Every Wizard Sally has heart of has been an owl.",
                'menu_illust': "Magical Opus",
                'location': "Sally's School Supplies",
                'required_classes': ['Wizard'],
                'reward_cards': ["Chimeric Wand"],
                'dialogue': [
                    {
                        'speaker': 'Sally',
                        'text': "And who would you be. Oh, a Wizard! Stupendous! Do come in, do come in! "
                                "You know, a brigand brought this wand back from the south a couple weeks ago. "
                                "She said it was very rare. Seems to me like something a wizard would like.",
                        'responses': [
                            "It was quite the adventure getting here",
                            "It was nothing",
                            "You sure have interesting curiosities",
                        ]
                    },
                ],
                'completion_log': "Sally met a Wizard. Received a Chimeric Wand card."
            },
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

def has_required_classes(required_classes, party):
    """Checks if party contains any of the required_classes."""

    for class_name in required_classes:
        for member in party.members:
            if class_name == member.current_class:
                break 
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

            meets_req_loc = is_location_match(req_loc, party.x, party.y)
            meets_req_cards = has_required_cards(req_cards_have + req_cards_give, party.inventory)
            meets_req_classes = has_required_classes(step_data.get('required_classes', []), party)

            if meets_req_loc and meets_req_cards and meets_req_classes:
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


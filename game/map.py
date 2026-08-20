import random
from .engine import Character

WORLD_MAP = [
    ["^", "S", "^", "^", "^", ".", ".", ".", ".", ".", ".", ".", ".", "↟", "↟"],
    ["R", "R", "^", "^", ".", ".", ".", ".", ".", ".", ".", ".", "↟", "↟", "↟"],
    ["^", "^", "^", "^", ".", ".", ".", ".", ".", ".", ".", ".", "↟", "↟", "↟"],
    ["^", "^", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "↟", "↟"],
    ["^", ".", ".", ".", ".", ".", "_", "_", "_", ".", ".", ".", ".", "↟", "↟"],
    ["^", ".", ".", ".", ".", ".", "S", "_", "I", ".", ".", ".", ".", "↟", "↟"],
    ["^", ".", ".", ".", ".", ".", "S", "_", "_", ".", ".", ".", ".", ".", "↟"],
    ["^", "^", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "↟", "↟"],
    ["^", "^", "^", ".", ".", ".", ".", ".", ".", ".", ".", "R", "↟", "↟", "↟"],
    ["^", "^", "^", "^", ".", ".", ".", ".", ".", ".", ".", "↟", "R", "↟", "↟"],
    ["^", "^", "^", "^", "^", ".", ".", ".", ".", ".", "↟", "↟", "↟", "↟", "↟"],
]

MAP_WIDTH = len(WORLD_MAP[0])
MAP_HEIGHT = len(WORLD_MAP)

TILE_DESCRIPTIONS = {
    'S': ('Shop', 'A bustling roadside merchant shop selling valuable items and move cards.'),
    'I': ('Inn', 'A cozy inn offering a place to rest, fully restore party HP, and organize companions.'),
    'R': ('Ancient Ruins', 'Dangerous crumbling stone ruins. Hostile forces and rare artifacts await!'),
    '^': ('Mountain Pass', 'Rugged, high-altitude mountain terrain filled with treacherous wild beasts.'),
    '↟': ('Dense Forest', 'Dark whispering woods where monsters stalk from the shadows.'),
    '.': ('Open Field', 'Quiet open grasslands along the main adventuring path.'),
    '_': ('In Town', 'Peaceful, well defended flagstone paths. The Rot won\'t get you here.'),
}

SHOP_DATA = [
    {
        'title': 'Wandering Potion Tortoise',
        'items': [
            ('Sour Potion', 30),
            ('Syrupy Potion', 20),
            ('Potion', 10),
        ],
        'illust': """
+--------------------------------------------------------/-----------------------------------------+
|                          /\                           /                        "                 |
|                         / `\_                        /  "                      "  "              |
|                        / ` ` \          /\          /  "            "                            |
|                       / ` \`` \        /``\        /                   "        "          "     |
|                      /~~~u~\~u~\      /~~~~\      /            ‖    ‖                            |
|                     /       \   \   _/  _   \    /  "  >%@====(O)==(O)========‖=====@%<   "      |
|                    /         \_  \ /   /     \_ /       /            ‖       (O)   / "           |
|                   /            \  \        __ _/ ___ >%@============(_)===========@%<     "      |
|                  /              \  \      / "" "" "   " "                                        |
+------------------------------------------/-------------------------------------------------------+
""",
        'dialogues': [
            ("Telly", "What am I doing up on this mountain? The kind of unlucky fool up here pays a lot more for " + 
            "their potions, he he he."),
            ("Telly", "Would you like a potion? They're delicious."),
            ("Telly", "Isn't that view gorgeous. Now if it weren't for all this Rot."),
        ]
    },
    {
        'title': 'Badgy\'s General Store',
        'items': [
            ('Honed Slash', 40),
            ('Honed Archery', 40),
            ('Shield', 15),
            ('Wax', 15),
            ('Potion', 5),
        ],
        'illust': """
+--------------------------------------------------------------------------------------------------+
| | || |                        \---/                                              |\|             |
|_|U||U|____                    |   |                                            . |/| .           |
|___________}                  / *   \                                         @=J=====J=@         |
|      \&/                    | o * * |                         __                | | |            |
|       U                     |   * o |                      __((@)_              | $ |            |
|                          ____\_____/______________________((@)-((@)__           | | |            |
|                         {____________________________________________}          | | |            |
|                          \|             |                    |     |/           |   |            |
|                           |       |                          @     |            |   |            |
+--------------------------------------------------------------------------------------------------+
""",
        'dialogues': [
            ("Badgy", "Welcome in! You know, brigands like yourself are becoming awfully popular with this Rot about. " +
            "I'm trying to stay stock with what you lot like. I hear there are lots of brigands out in the woods; " +
            "Maybe you all should team up, fight the Rot together." )
        ]
    },
    {
        'title': 'Sally\'s School Supplies',
        'items': [
            ('Training', 50),
            ('Study', 50),
            ('Elementary Magic', 60),
            ('Simple Trap', 60),
            ('Bargain', 15),
        ],
        'illust': """
+--------------------------------------------------------------------------------------------------+
| | || |                        \---/                                              |\|             |
|_|U||U|____                    |   |                                            . |/| .           |
|___________}                  / *   \                                         @=J=====J=@         |
|      \&/                    | o * * |                         __                | | |            |
|       U                     |   * o |                      __((@)_              | $ |            |
|                          ____\_____/______________________((@)-((@)__           | | |            |
|                         {____________________________________________}          | | |            |
|                          \|             |                    |     |/           |   |            |
|                           |       |                          @     |            |   |            |
+--------------------------------------------------------------------------------------------------+
""",
        'dialogues': [
            ("Sally", "Learning's a wonderful thing, isn't it? Be carefuly though; get too close to " + 
            "some these things and you just might not recognize yourself."),
            ("Sally", "Oh! You're a brigand! Well I never! Don't you worry, I'm sure we can find " + 
            "something that'll make you a new person in no time!")
        ]
    },
]

INN_DATA = [
    {
        'id': 'inn_0',
        'title': 'The Cozy Salmon Inn',
        'illust': """
+--------------------------------------------------------------------------------------------------+
|                                                                                   ==)===)========|
|                                                                                     O   O        |
|                                                                                    ()  ()        |
|                                                                                   /-n---n-\      |
|                                                                                   |  INN  |      |
|                                                                                   |  ===  /      |
|                                                                                   +------/       |
|                                                                                                  |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
""",
        'dialogues': [
            ("Innkeeper Barnaby", "Welcome, weary travelers! Rest your head, heal your wounds, and organize your company."),
            ("Innkeeper Barnaby", "The Rot might be fierce outside, but our hearth is warm and safe."),
        ]
    },
]

ALL_PLAYABLE_SPECIES = [
    'Fox', 'Cat', 'Badger', 'Rabbit', 'Owl', 'Raven',
    'Dragonling', 'Ember Sprite', 'Dew Sprite', 'Loss Sprite', 'Clockwork'
]

DEFAULT_CHARACTER_NAMES = [
    'Twig', 'Lily', 'Pip', 'Moss', 'Bramble', 'Clover', 'Hazel', 'Fern',
    'Rowan', 'Acorn', 'Willow', 'Pebble', 'Finley', 'Copper', 'Oat',
    'Thistle', 'Sedge', 'Cedar', 'Birch', 'Briar', 'Plum', 'Pippin', 'Sprout'
]

DEFAULT_CLASS_STARTER_CARDS = {
    'Student': {
        'trinket': ['Study'],
        'scroll': ['Elementary Magic', 'Wain', 'Wax', 'Singe', 'Chill'],
    },
    'Squire': {
        'weapon': ['Favorite Slash', 'Favorite Heavy Slash', 'Favorite Light Slash'],
        'trinket': ['Training', 'First Aid'],
    },
    'Scout': {
        'trinket': ['First Aid'],
        'weapon': ['Favorite Archery', 'Simple Trap'],
    },
}

ENCOUNTER_DATA = {
    '.': [
        {
            'chance': 0.1,
            'min_enemies': 1,
            'max_enemies': 1,
            'species': ALL_PLAYABLE_SPECIES,
            'classes': ['Student', 'Squire', 'Scout'],
            'target_level': 2,
            'is_recruitable': True,
            'cards_by_class': DEFAULT_CLASS_STARTER_CARDS,
            'names': DEFAULT_CHARACTER_NAMES,
        },
        {
            'chance': 0.2,
            'min_enemies': 2,
            'max_enemies': 2,
            'species': ['Badger', 'Cat', 'Fox', 'Rabbit', 'Owl'],
            'classes': ['Husk']
        },
        {
            'chance': 0.1,
            'min_enemies': 2,
            'max_enemies': 2,
            'species': ['Badger', 'Cat', 'Fox', 'Owl'],
            'classes': ['Husk', 'Soul']
        },
    ],
    'R': [
        {
            'chance': 1,
            'min_enemies': 3,
            'max_enemies': 4,
            'species': ['Badger', 'Cat', 'Fox', 'Rabbit', 'Owl'],
            'classes': ['Husk', 'Soul', 'Rotmonger']
        },
    ],
    '^': [
        {
            'chance': 0.6,
            'min_enemies': 2,
            'max_enemies': 4,
            'species': ['Badger', 'Cat', 'Fox', 'Rabbit', 'Owl'],
            'classes': ['Husk', 'Soul', 'Rotmonger']
        }
    ],
    '↟': [
        {
            'chance': 0.3,
            'min_enemies': 1,
            'max_enemies': 1,
            'species': ALL_PLAYABLE_SPECIES,
            'classes': ['Student', 'Squire', 'Scout'],
            'target_level': 4,
            'is_recruitable': True,
            'cards_by_class': DEFAULT_CLASS_STARTER_CARDS,
            'names': DEFAULT_CHARACTER_NAMES,
        },
        {
            'chance': 0.5,
            'min_enemies': 2,
            'max_enemies': 4,
            'species': ['Badger', 'Cat', 'Fox', 'Rabbit', 'Owl'],
            'classes': ['Husk', 'Soul', 'Rotmonger']
        }
    ],
    '_': [ ]
}

def get_shop(shop_x, shop_y):

    map = WORLD_MAP
    idx = 0

    for y in range(len(map)):
        for x in range(len(map[y])):
            if x == shop_x and y == shop_y:
                return SHOP_DATA[min(idx, len(SHOP_DATA)-1)]
            elif map[y][x] == 'S': 
                idx += 1

def get_inn(inn_x, inn_y):
    map_grid = WORLD_MAP
    idx = 0
    for y in range(len(map_grid)):
        for x in range(len(map_grid[y])):
            if x == inn_x and y == inn_y:
                inn_info = dict(INN_DATA[min(idx, len(INN_DATA) - 1)])
                inn_info['index'] = idx
                return inn_info
            elif map_grid[y][x] == 'I':
                idx += 1
    return None

def get_inn_id(inn_x, inn_y):
    inn_info = get_inn(inn_x, inn_y)
    return inn_info.get('id') if inn_info else None

def get_nearest_inn_id(px, py):
    map_grid = WORLD_MAP
    idx = 0
    nearest_id = None
    min_dist = float('inf')
    
    for y in range(len(map_grid)):
        for x in range(len(map_grid[y])):
            if map_grid[y][x] == 'I':
                dist = abs(px - x) + abs(py - y)
                if dist < min_dist:
                    min_dist = dist
                    inn_info = INN_DATA[min(idx, len(INN_DATA) - 1)]
                    nearest_id = inn_info.get('id')
                idx += 1
    return nearest_id or INN_DATA[0].get('id', 'inn_0')


def generate_random_enemies(encounter_data):
    """Generates enemy characters using the exact Character system."""
    count = random.randint(encounter_data['min_enemies'], encounter_data['max_enemies'])
    
    species_options = encounter_data['species']
    class_options = encounter_data['classes']
    cards_by_class = encounter_data.get('cards_by_class', {})
    target_lvl = encounter_data.get('target_level')

    names = list(encounter_data.get('names', []))
    random.shuffle(names)

    enemies = []
    for i in range(count):
        sp = random.choice(species_options)
        cl = random.choice(class_options)
        
        name = "{0} {1}".format(sp, cl)
        if names:
            name = names.pop()

        enemy = Character(name=name, species=sp, current_class=cl, level=1)

        if cards_by_class and cl in cards_by_class:
            class_pools = cards_by_class[cl]
            for card_type in class_pools:
                chosen_card = random.choice(class_pools[card_type])
                enemy.give_card(chosen_card)

        if target_lvl is not None:
            while enemy.get_scaled_stats().get('level') < target_lvl:
                enemy.give_card('Potion')

        enemy.current_hp = enemy.max_hp
        enemies.append(enemy)
    return enemies

def get_random_encounter(encounter_x, encounter_y):
    terrain = WORLD_MAP[encounter_y][encounter_x]
    encounter_data = ENCOUNTER_DATA.get(terrain, [])
    r = random.random()
    for encounter in encounter_data:
        if r < encounter['chance']:
            enemies = generate_random_enemies(encounter)
            return enemies, encounter.get('is_recruitable', False)
        r -= encounter['chance']
    return [], False

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
            ('Simple Trap', 60),
            ('Elementary Magic', 60),
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

ENCOUNTER_DATA = {
    '.': [
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
                return SHOP_DATA[min(idx, len(SHOP_DATA))]
            elif map[y][x] == 'S': 
                idx += 1

def generate_random_enemies(encounter_data, level=1):
    """Generates enemy characters using the exact Character system."""
    count = random.randint(encounter_data['min_enemies'], encounter_data['max_enemies'])
    
    species_options = encounter_data['species']
    class_options = encounter_data['classes']

    enemies = []
    for i in range(count):
        sp = random.choice(species_options)
        cl = random.choice(class_options)
        name = f"{sp} {cl}"
        enemy = Character(name=name, species=sp, current_class=cl, level=level)
        enemies.append(enemy)
    return enemies

def get_random_encounter(encounter_x, encounter_y, level=1):
    terrain = WORLD_MAP[encounter_y][encounter_x]
    encounter_data = ENCOUNTER_DATA[terrain]
    r = random.random()
    for encounter in encounter_data:
        if r < encounter['chance']:
            return generate_random_enemies(encounter, level)
        r -= encounter['chance']
    return []

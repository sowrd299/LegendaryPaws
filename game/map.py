import random
from .engine import Character, CLASS_DATA


VIEWPORT_MAX_WIDTH = 15
VIEWPORT_MAX_HEIGHT = 15


def calculate_map_pan(party_x, party_y, current_pan_x=None, current_pan_y=None):
    """Calculates viewport pan_x and pan_y keeping player within a 5x5 center deadzone of the viewport."""
    min_x = get_map_min_x()
    max_x = get_map_max_x()
    min_y = get_map_min_y()
    max_y = get_map_max_y()
    map_w = max_x - min_x
    map_h = max_y - min_y

    vw = min(VIEWPORT_MAX_WIDTH, map_w)
    vh = min(VIEWPORT_MAX_HEIGHT, map_h)

    max_pan_x = max(min_x, max_x - vw)
    max_pan_y = max(min_y, max_y - vh)

    # Center box definition (5 wide x 5 high centered inside viewport)
    center_x = vw // 2
    min_cx = center_x - 2
    max_cx = center_x + 2

    center_y = vh // 2
    min_cy = center_y - 2
    max_cy = center_y + 2

    # Calculate pan_x
    if current_pan_x is None:
        pan_x = max(min_x, min(max_pan_x, party_x - center_x))
    else:
        pan_x = current_pan_x
        local_x = party_x - pan_x
        if local_x < min_cx:
            pan_x = max(min_x, party_x - min_cx)
        elif local_x > max_cx:
            pan_x = min(max_pan_x, party_x - max_cx)

    # Calculate pan_y
    if current_pan_y is None:
        pan_y = max(min_y, min(max_pan_y, party_y - center_y))
    else:
        pan_y = current_pan_y
        local_y = party_y - pan_y
        if local_y < min_cy:
            pan_y = max(min_y, party_y - min_cy)
        elif local_y > max_cy:
            pan_y = min(max_pan_y, party_y - max_cy)

    return pan_x, pan_y


DEFAULT_TILE_DESCRIPTIONS = {
    'S': ('Shop', 'A bustling roadside merchant shop selling valuable items and move cards.'),
    'I': ('Inn', 'A cozy inn offering a place to rest, fully restore party HP, and organize companions.'),
    'R': ('Ancient Ruins', 'Dangerous crumbling stone ruins. Hostile forces and rare artifacts await!'),
    '^': ('Mountain Pass', 'Rugged, high-altitude mountain terrain filled with treacherous wild beasts.'),
    'f': ('Dense Forest', 'Dark whispering woods where monsters stalk from the shadows.'),
    '.': ('Open Field', 'Quiet open grasslands along the main adventuring path.'),
}

SHOP_DATA = [
]


DEFAULT_START_INN_ID = 'inn_0'

ALL_PLAYABLE_SPECIES = [
    'Fox', 'Cat', 'Badger', 'Rabbit', 'Owl', 'Raven',
    'Dragonling', 'Ember Sprite', 'Dew Sprite', 'Loss Sprite', 'Clockwork'
]

DEFAULT_CHARACTER_NAMES = [
    'Twig', 'Lily', 'Pip', 'Moss', 'Bramble', 'Clover', 'Hazel', 'Fern',
    'Rowan', 'Acorn', 'Willow', 'Pebble', 'Finley', 'Copper', 'Oat',
    'Thistle', 'Sedge', 'Cedar', 'Birch', 'Briar', 'Plum', 'Pippin', 'Sprout',
    'Thimble', 
]

DEFAULT_CLASS_STARTER_CARDS = {
    'Student': {
        'scroll': ['Elementary Magic', 'Wain', 'Singe', 'Chill'],
        'armor': ['Favored Clothes', 'Student\'s Robes'],
    },
    'Squire': {
        'weapon': ['Favored Slash', 'Favored Heavy Slash', 'Favored Light Slash'],
        'armor': ['Favored Clothes', 'Shield', 'Shield Spike'],
    },
    'Scout': {
        'weapon': ['Favored Archery', 'Simple Trap', 'Pinning Shot'],
        'trinket': ['Quiver Quickdraw'],
    },
}

DEFAULT_REWARD_CARDS = [
    
    # Defense
    'Potion', 
    'Potion', 
    'Light Clothes', 
    'Light Clothes', 
    'Shield',

    # Squire
    'Slash', 
    'Slash', 
    'Slash', 
    'Slash', 
    'Light Slash', 
    'Shield Spike',

    # Scout
    'Archery', 
    'Heavy Shot',
    'Whistling Shot',
    'Crescent Shot',
    'Burning Shot',
    'Broken Shot',

    # Student
    'Wain', 
    'Wax', 
    'Singe', 
    'Singe Breath', 
    'Chill', 
    'Chill Breath',
]

DEFAULT_ODD_REWARD_CARDS = [
    'Pinning Shot',
    'Waxing Moonlight',
    'Singeing Sunlight',
    'Call to the Void',
    'Battlesong',
]


def default_encounter_data(target_level): 

    reward_cards = list(DEFAULT_REWARD_CARDS)
    if target_level >= 4:
        reward_cards += DEFAULT_ODD_REWARD_CARDS

    return [
        {
            'chance': 0.1,
            'min_enemies': 1,
            'max_enemies': 1,
            'species': ALL_PLAYABLE_SPECIES,
            'classes': ['Student', 'Squire', 'Scout'],
            'target_level': target_level + 2,
            'is_recruitable': True,
            'cards_by_class': DEFAULT_CLASS_STARTER_CARDS,
            'names': DEFAULT_CHARACTER_NAMES,
            'reward_cards': reward_cards
        },
        {
            'chance': 0.5,
            'min_enemies': 3,
            'max_enemies': 4,
            'target_level': target_level,
            'species': ['Badger', 'Cat', 'Fox', 'Rabbit', 'Owl', 'Raven', 'Dragonling', 'Giant'],
            'classes': ['Hollow', 'Essence', 'Rotmonger'],
            'reward_cards': reward_cards
        }
    ]


DEFAULT_SHOP_ILLUST = """
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
"""


class MapZone:
    def __init__(self, grid, offset_x=0, offset_y=0, shop_data=None, inn_data=None, encounter_data=None, tile_descriptions=None):
        self.grid = grid
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.shop_data = shop_data if shop_data is not None else []
        self.inn_data = inn_data if inn_data is not None else []
        self.encounter_data = encounter_data if encounter_data is not None else {}
        self.tile_descriptions = tile_descriptions if tile_descriptions is not None else {}

    @property
    def width(self):
        return len(self.grid[0]) if self.grid else 0

    @property
    def height(self):
        return len(self.grid) if self.grid else 0

    def defines_space(self, x, y):
        lx = x - self.offset_x
        ly = y - self.offset_y
        if 0 <= ly < len(self.grid) and 0 <= lx < len(self.grid[ly]):
            return self.grid[ly][lx] != ' '
        return False

    def get_tile(self, x, y):
        lx = x - self.offset_x
        ly = y - self.offset_y
        if 0 <= ly < len(self.grid) and 0 <= lx < len(self.grid[ly]):
            return self.grid[ly][lx]
        return ' '

    def get_tile_description(self, x, y):
        tile = self.get_tile(x, y)
        return self.tile_descriptions.get(tile, ('Unknown', 'A mysterious land.'))

    def should_reset_losable_gold(self, x, y):
        if self.get_tile(x, y) == '_':
            return True
        shop = self.get_shop(x, y)
        if shop and shop.get('should_reset_losable_gold', False):
            return True
        inn = self.get_inn(x, y)
        if inn and inn.get('should_reset_losable_gold', False):
            return True
        return False

    def get_shop(self, shop_x, shop_y):
        idx = 0
        for ly in range(len(self.grid)):
            for lx in range(len(self.grid[ly])):
                if self.grid[ly][lx] == 'S':
                    gx = lx + self.offset_x
                    gy = ly + self.offset_y
                    if gx == shop_x and gy == shop_y:
                        if self.shop_data:
                            return self.shop_data[min(idx, len(self.shop_data) - 1)]
                        return None
                    idx += 1
        return None

    def get_inn(self, inn_x, inn_y):
        idx = 0
        for ly in range(len(self.grid)):
            for lx in range(len(self.grid[ly])):
                if self.grid[ly][lx] == 'I':
                    gx = lx + self.offset_x
                    gy = ly + self.offset_y
                    if gx == inn_x and gy == inn_y:
                        if self.inn_data:
                            inn_info = dict(self.inn_data[min(idx, len(self.inn_data) - 1)])
                            inn_info['index'] = idx
                            return inn_info
                        return None
                    idx += 1
        return None

    def get_inn_id(self, inn_x, inn_y):
        inn_info = self.get_inn(inn_x, inn_y)
        return inn_info.get('id') if inn_info else None

    def get_inn_coords(self, inn_id):
        idx = 0
        for ly in range(len(self.grid)):
            for lx in range(len(self.grid[ly])):
                if self.grid[ly][lx] == 'I':
                    gx = lx + self.offset_x
                    gy = ly + self.offset_y
                    if self.inn_data:
                        current_id = self.inn_data[min(idx, len(self.inn_data) - 1)].get('id')
                        if current_id == inn_id:
                            return (gx, gy)
                    idx += 1
        return None

    def get_nearest_inn_id(self, px, py):
        idx = 0
        nearest_id = None
        min_dist = float('inf')
        for ly in range(len(self.grid)):
            for lx in range(len(self.grid[ly])):
                if self.grid[ly][lx] == 'I':
                    gx = lx + self.offset_x
                    gy = ly + self.offset_y
                    dist = abs(px - gx) + abs(py - gy)
                    if dist < min_dist:
                        min_dist = dist
                        if self.inn_data:
                            nearest_id = self.inn_data[min(idx, len(self.inn_data) - 1)].get('id')
                    idx += 1
        return min_dist, nearest_id

    def get_random_encounter(self, encounter_x, encounter_y):
        terrain = self.get_tile(encounter_x, encounter_y)
        encounter_data = self.encounter_data.get(terrain, [])
        r = random.random()
        for encounter in encounter_data:
            if r < encounter['chance']:
                enemies = generate_random_enemies(encounter)
                reward_card = random.choice(encounter.get('reward_cards', DEFAULT_REWARD_CARDS))
                reward_gold = random.randint(encounter.get('reward_min_gold', 5), encounter.get('reward_max_gold', 10))

                return enemies, encounter.get('is_recruitable', False), reward_card, reward_gold
            r -= encounter['chance']
        return [], False, None, 0


MAP_ZONES = [
    
    # The Starting Zone
    MapZone(
        grid=[
            "^^^^^^^^....f..ffff",
            "^^^^^^^^^.....fffff",
            "^^^^R^^^...f...ffff",
            "^R^S^^^........ffff",
            "^^RR^^...   ..fffff",
            "R^^^^^...   ..fffff",
            "^^^^...........ffff",
            "^^^.....___....ffff",
            "^^^.....S_I....ffff",
            "^^^.....___.....fff",
            "^^^^...........ffff",
            "^.^^^........Rfffff",
            "^..^^^.......fRffff",
            "..^^^^^.....fff.fff",
            "..^^^^.....fff...ff",
            "..^^^.....fffff.fff",
            "..^^..^..ffffffffff",
        ],
        offset_x=0,
        offset_y=0,
        shop_data=[
            {
                'title': 'Wandering Potion Tortoise',
                'items': [
                    ('Sour Potion', 30),
                    ('Syrupy Potion', 20),
                    ('Potion', 10),
                    ('Bargain', 50),
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
                'illust': DEFAULT_SHOP_ILLUST,
                'dialogues': [
                    ("Badgy", "Welcome in! You know, brigands like yourself are becoming awfully popular with this Rot about. " +
                    "I'm trying to stay stock with what you lot like. I hear there are lots of brigands out in the woods; " +
                    "Maybe you all should team up, fight the Rot together." )
                ],
                'should_reset_losable_gold': True
            }
        ],
        inn_data=[
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
                    ("Innkeeper", "Welcome, weary travelers! Rest your heads, heal your wounds, and organize your company."),
                    ("Innkeeper", "The Rot might be fierce outside, but our hearth is warm and safe, I promise."),
                ], 
                'should_reset_losable_gold': True,
            },
        ],
        encounter_data= {
            '.': [
                {
                    'chance': 0.2,
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
                    'chance': 0.1,
                    'min_enemies': 2,
                    'max_enemies': 2,
                    'species': ['Cat', 'Fox', 'Rabbit', 'Owl', 'Raven', 'Dragonling'],
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
                    'chance': 0.8,
                    'min_enemies': 3,
                    'max_enemies': 4,
                    'species': ['Badger', 'Cat', 'Fox', 'Rabbit', 'Raven', 'Giant'],
                    'classes': ['Husk', 'Rotmonger'],
                    'reward_cards': DEFAULT_ODD_REWARD_CARDS,
                },
                {
                    'chance': 0.2,
                    'min_enemies': 1,
                    'max_enemies': 1,
                    'species': ['Dragon'],
                    'classes': ['Matron'],
                    'reward_min_gold': 60,
                    'reward_max_gold': 80,
                    'reward_cards': ['Dragonsbane'],
                    'names': ['Rotmatron'],
                },
            ],
            '^': [
                {
                    'chance': 0.3,
                    'min_enemies': 2,
                    'max_enemies': 4,
                    'species': ['Badger', 'Cat', 'Fox', 'Rabbit', 'Owl'],
                    'classes': ['Husk', 'Soul', 'Rotmonger'],
                    'reward_cards': DEFAULT_REWARD_CARDS + DEFAULT_ODD_REWARD_CARDS,
                },
                {
                    'chance': 0.3,
                    'min_enemies': 2,
                    'max_enemies': 4,
                    'species': ['Cat', 'Fox', 'Rabbit', 'Giant'],
                    'classes': ['Husk'],
                    'reward_cards': DEFAULT_REWARD_CARDS + DEFAULT_ODD_REWARD_CARDS,
                }
            ],
            'f': [
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
                    'classes': ['Husk', 'Soul', 'Rotmonger'],
                    'reward_cards': DEFAULT_REWARD_CARDS + ['Flowering Stab'],
                }
            ],
            '_': [ ]
        },
        tile_descriptions=dict(DEFAULT_TILE_DESCRIPTIONS, **{
            '_': ('New Dunton Village', 'Peaceful, well defended flagstone paths. The Rot won\'t get you here.'),
        }),
    ),

    # The "rotten egg dragonslings" map zone
    MapZone(
        grid = ["...", "..."],
        offset_x = 9,
        offset_y = 4,
        encounter_data = {
            '.': [
                {
                    'chance': .5,
                    'min_enemies': 2,
                    'max_enemies': 3,
                    'species': ['Dragonling'],
                    'classes': ['Husk'],
                    'reward_cards': ["Rotten Egg"],
                },
            ],
       },
       
       tile_descriptions = DEFAULT_TILE_DESCRIPTIONS, 
    ),

    # The zone across the mountains from Dunton
    MapZone(
        grid=[
                "..................^",
                ".........______....",
                ".......~~_S_SI_...^",
                "......~~~______...^",
                ".......~~___.......",
                ".........___......^",
                "...............R.^^",
                "..............R.^^^",
                "................^^^",
                "............R..^.^^",
                ".................^^",
                "..f.ff........R...^",
                ".fffffff........^^.",
                "f   fffff........^.",
                "f   ffffff.....^...",
                "f   fffff..f..f....",
                "ffffffffff...fff...",
        ],
        offset_x=-19,
        offset_y=0,
        shop_data=[
            {
                'title': 'Sally\'s School Supplies',
                'items': [
                    ('Training', 50),
                    ('Study', 50),
                    ('Elementary Magic', 60),
                    ('Simple Trap', 60),
                ],
                'illust': DEFAULT_SHOP_ILLUST,
                'dialogues': [
                    ("Sally", "Learning's a wonderful thing, isn't it? Be carefuly though; get too close to " + 
                    "some these things and you just might not recognize yourself."),
                    ("Sally", "Oh! You're a brigand! Well I never! Don't you worry, I'm sure we can find " + 
                    "something that'll make you a new person in no time!")
                ],
                'should_reset_losable_gold': True,
            },
            {
                'title': 'Hemlock\'s Miscellany',
                'items': [
                    ('Light Clothes', 15),
                    ('Shield', 15),
                    ('Potion', 5),
                    ('Rotten Egg', 20)
                ],
                'illust': DEFAULT_SHOP_ILLUST,
                'dialogues': [
                    ("Old Man Hemlock", "Oh, you came from Dunton you say? Not many people cross the little mountains now that they're all covered in Rot. " +
                    "Just brigands that mad tortoise by my count."),
                ],
                'should_reset_losable_gold': True
            }
        ],
        inn_data=[
            {
                'id': 'inn_1',
                'title': 'The Quilted Dragonfly Inn',
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
                    ("Innkeeper", "Welcome, weary travelers! Rest your heads, heal your wounds, and organize your company."),
                    ("Innkeeper", "The Rot might be fierce outside, but our hearth is warm and safe, I promise."),
                ], 
                'should_reset_losable_gold': True,
            },
        ],
        encounter_data = {
            '.': default_encounter_data(1),
            '^': default_encounter_data(2),
            'R': default_encounter_data(7),
            'f': default_encounter_data(4),
            '_': [],
        },
        tile_descriptions=dict(DEFAULT_TILE_DESCRIPTIONS, **{
            '_': ('The Village of Yonder', 'A quiet village in the shadow of the little mountains.'),
            '~': ('Yonder Springs', 'a warm, softly rippling pool in the plains')
        }),
    ),

    # The Sprite Village
    MapZone(
        grid=[
                "Sff",
                "fff",
                "ffS",
        ],
        offset_x=-18,
        offset_y=13,
        shop_data=[
            {
                'title': 'Wands for Wanderers',
                'items': [
                    ('Ash Wand', 100),
                    ('Driftwood Wand', 100),
                    ('Fossil Wand', 100),
                ],
                'illust': DEFAULT_SHOP_ILLUST,
                'dialogues': [
                    ("Wand Selling Sprite", "A bad mage can't use a wand, a better mage is even better with one, a great mage doesn't have hands, a mediocre mage " +
                    "is a menance with a wand, a middling mage with a want is a question of if they figure out which end is up..."),
                    ("Wand Selling Sprite", "We used to have visitors of the other folks all the time, then they went on about a sudden \"Rot\" and we've barely seen " +
                    "anyone since. Say, are you Rotten? Is that why you're here? Hard to tell with that bizzar body of yours."),
                ],
                'should_reset_losable_gold': False,
            },
            {
                'title': 'Scrolls for Scoundrels',
                'items': [
                    ('New Moon', 100)
                ],
                'illust': DEFAULT_SHOP_ILLUST,
                'dialogues': [
                    ("Scroll Selling Sprite", "We used to have visitors of the other folks all the time, then they went on about a sudden \"Rot\" and we've barely seen " +
                    "anyone since. Say, are you Rotten? Is that why you're here? Hard to tell with that bizzar body of yours."),
                ],
                'should_reset_losable_gold': False, 
            }
        ],
        encounter_data={
            '.': [
                {
                    'chance': .2,
                    'min_enemies': 1,
                    'max_enemies': 3,
                    'species': ['Ember Sprite', 'Dew Sprite', 'Loss Sprite'],
                    'classes': ['Day Mage', 'Night Mage', 'Passage Mage'],
                    'cards_by_class': {
                        'Day Mage': {
                            'weapon': ['Ash Wand'],
                            'scroll': ['Singe Breath', 'Singeing Sunlight'],
                        },
                        'Night Mage': {
                            'weapon': ['Driftwood Wand'],
                            'scroll': ['Wain', 'Woe'],
                        },
                        'Passage Mage': {
                            'weapon': ['Fossil Wand'],
                            'scroll': ['Chill Breath', 'Call to the Void'],
                        },
                    },
                    'target_level': 5,
                    'reward_cards': DEFAULT_ODD_REWARD_CARDS,
                },
                {
                    'chance': .2,
                    'min_enemies': 1,
                    'max_enemies': 3,
                    'species': ['Ember Sprite', 'Dew Sprite', 'Loss Sprite'],
                    'classes': ['Day Mage', 'Night Mage', 'Passage Mage'],
                    'cards_by_class': {
                        'Day Mage': {
                            'weapon': ['Ash Wand'],
                            'scroll': ['Singe Breath', 'Singeing Sunlight'],
                        },
                        'Night Mage': {
                            'weapon': ['Driftwood Wand'],
                            'scroll': ['Wain', 'Woe'],
                        },
                        'Passage Mage': {
                            'weapon': ['Fossil Wand'],
                            'scroll': ['Chill Breath', 'Call to the Void'],
                        },
                    },
                    'target_level': 5,
                    'is_recruitable': True,
                    'reward_cards': DEFAULT_ODD_REWARD_CARDS,
                },
            ],
        },
        tile_descriptions=dict(DEFAULT_TILE_DESCRIPTIONS, **{
            'f': ('The Hamlet of the Sprites', 'An eclectic home in the forest; both a testament to their magical craft, and a study in their lack of understanding of mortal needs or mortal fear. Many spites welcome outsiders into the hamlet, but many do not.'),
        }),
    ),
]


def get_zone_for_space(x, y):
    for zone in MAP_ZONES:
        if zone.defines_space(x, y):
            return zone
    return None


def get_map_min_x():
    if not MAP_ZONES:
        return 0
    return min(zone.offset_x for zone in MAP_ZONES)


def get_map_max_x():
    if not MAP_ZONES:
        return 0
    return max(zone.offset_x + zone.width for zone in MAP_ZONES)


def get_map_min_y():
    if not MAP_ZONES:
        return 0
    return min(zone.offset_y for zone in MAP_ZONES)


def get_map_max_y():
    if not MAP_ZONES:
        return 0
    return max(zone.offset_y + zone.height for zone in MAP_ZONES)


def get_map_width():
    return get_map_max_x() - get_map_min_x()


def get_map_height():
    return get_map_max_y() - get_map_min_y()


def get_tile(x, y):
    zone = get_zone_for_space(x, y)
    if zone:
        return zone.get_tile(x, y)
    return ' '


def get_tile_description(x, y):
    zone = get_zone_for_space(x, y)
    if zone:
        return zone.get_tile_description(x, y)
    return ('Unknown', 'A mysterious land.')


def should_reset_losable_gold(x, y):
    zone = get_zone_for_space(x, y)
    if zone:
        return zone.should_reset_losable_gold(x, y)
    return False


def get_shop(shop_x, shop_y):
    zone = get_zone_for_space(shop_x, shop_y)
    if zone:
        return zone.get_shop(shop_x, shop_y)
    return None


def get_inn(inn_x, inn_y):
    zone = get_zone_for_space(inn_x, inn_y)
    if zone:
        return zone.get_inn(inn_x, inn_y)
    return None


def get_inn_id(inn_x, inn_y):
    zone = get_zone_for_space(inn_x, inn_y)
    if zone:
        return zone.get_inn_id(inn_x, inn_y)
    return None


def get_inn_coords(inn_id):
    for zone in MAP_ZONES:
        coords = zone.get_inn_coords(inn_id)
        if coords:
            gx, gy = coords
            if get_zone_for_space(gx, gy) == zone:
                return (gx, gy)
    # Fallback to first inn on map where space is defined by its zone
    for zone in MAP_ZONES:
        for ly in range(len(zone.grid)):
            for lx in range(len(zone.grid[ly])):
                if zone.grid[ly][lx] == 'I':
                    gx = lx + zone.offset_x
                    gy = ly + zone.offset_y
                    if get_zone_for_space(gx, gy) == zone:
                        return (gx, gy)
    return (0, 0)


def get_nearest_inn_id(px, py):
    nearest_id = None
    min_dist = float('inf')
    fallback_id = None

    for zone in MAP_ZONES:
        idx = 0
        for ly in range(len(zone.grid)):
            for lx in range(len(zone.grid[ly])):
                if zone.grid[ly][lx] == 'I':
                    gx = lx + zone.offset_x
                    gy = ly + zone.offset_y
                    if get_zone_for_space(gx, gy) == zone:
                        if zone.inn_data:
                            i_id = zone.inn_data[min(idx, len(zone.inn_data) - 1)].get('id')
                            if fallback_id is None:
                                fallback_id = i_id
                            dist = abs(px - gx) + abs(py - gy)
                            if dist < min_dist:
                                min_dist = dist
                                nearest_id = i_id
                    idx += 1

    return nearest_id or fallback_id or 'inn_0'


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
        cl = random.choice(class_options)
        sp = random.choice([species for species in species_options if species in CLASS_DATA.get(cl, {}).get('enemy_species', species_options)])
        
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
    zone = get_zone_for_space(encounter_x, encounter_y)
    if zone:
        return zone.get_random_encounter(encounter_x, encounter_y)
    return [], False, None, 0


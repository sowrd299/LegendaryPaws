WORLD_MAP = [
    ["^", "S", "^", "^", "^", ".", ".", ".", ".", ".", ".", ".", ".", "↟", "↟"],
    ["R", "R", "^", "^", ".", ".", ".", ".", ".", ".", ".", ".", "↟", "↟", "↟"],
    ["^", "^", "^", "^", ".", ".", ".", ".", ".", ".", ".", ".", "↟", "↟", "↟"],
    ["^", "^", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "↟", "↟"],
    ["^", ".", ".", ".", ".", ".", "_", "_", "_", ".", ".", ".", ".", "↟", "↟"],
    ["^", ".", ".", ".", ".", ".", "S", "_", "I", ".", ".", ".", ".", "↟", "↟"],
    ["^", ".", ".", ".", ".", ".", "_", "_", "_", ".", ".", ".", ".", ".", "↟"],
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
|                               \---/                                              |\|             |
|                               |   |                                            . |/| .           |
|                              / *   \                                         @=J=====J=@         |
|                             | o * * |                         __                | | |            |
|                             |   * o |                      __((@)_              | $ |            |
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
    }
]

def get_shop(shop_x, shop_y):

    map = WORLD_MAP
    idx = 0

    for y in range(len(map)):
        for x in range(len(map[y])):
            if x == shop_x and y == shop_y:
                return SHOP_DATA[min(idx, len(SHOP_DATA))]
            elif map[y][x] == 'S': 
                idx += 1

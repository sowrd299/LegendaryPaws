import math
import random
import uuid
from .illustration import ILLUSTRATION_DATA

# --- STAT & MATH SCALING ---

CORE_STATS = ['level', 'brute_intensity', 'brute_resistance', 'nimbleness', 'haleness']

MAGIC_STATS = [
    'moon_intensity', 'moon_resistance', 'moon_vulnerability',
    'star_intensity', 'star_resistance', 'star_vulnerability',
    'void_intensity', 'void_resistance', 'void_vulnerability',
]

ALL_STATS = CORE_STATS + MAGIC_STATS + [
    'melee_damage', 'melee_resistance', 'melee_vulnerability',
    'ranged_damage', 'ranged_resistance', 'ranged_vulnerability',
    'survival_intensity', 'survival_resistance', 'survival_vulnerability',
    'diplomacy'
]

RARITIES = ['mundane', 'interesting', 'odd', 'exceptional', 'peerless']

DECK_MINIMUM_SIZE = 10

def raw_to_scaled(raw_val):

    is_negative = False
    if raw_val <= 0:
        is_negative = True
        raw_val *= -1

    scaled = math.sqrt(raw_val)
    return min(20, max(0, int(math.floor(scaled)))) * (-1 if is_negative else 1)

def scaled_to_raw(scaled_val):
    return (scaled_val) ** 2

# --- DATA DEFINITIONS: SPECIES & CLASSES ---

SPECIES_DATA = {
    'Fox': {'brute_intensity': 3, 'nimbleness': 3.0, 'haleness': 2.0, 'brute_resistance': 2.0},
    'Cat': {'brute_intensity': 3, 'nimbleness': 4.0, 'haleness': 3.0, 'brute_resistance': 1.0},
    'Badger': {'brute_intensity': 8, 'brute_resistance': 4.0, 'nimbleness': 1.0, 'haleness': 3.0},
    'Rabbit': {'brute_intensity': 3, 'nimbleness': 4.0, 'haleness': 2.0, 'brute_resistance': 0},
    'Owl': {'haleness': 3.0, 'star_intensity': 4.0, 'nimbleness': 2.0, 'brute_intensity': 3},
    'Raven': {'void_intensity': 4.0, 'nimbleness': 3.0, 'haleness': 2.0, 'brute_resistance': 1.0},
    'Dragonling': {'brute_intensity': 8, 'star_intensity': 3.0, 'haleness': 3.0, 'brute_resistance': 2.0},
    'Ember sprite': {'star_intensity': 5.0, 'star_resistance': 4.0, 'haleness': 1.0, 'brute_intensity': 0},
    'Dew sprite': {'moon_intensity': 5.0, 'moon_resistance': 4.0, 'haleness': 1.0, 'brute_intensity': 0},
    'Lost sprite': {'void_intensity': 5.0, 'void_resistance': 4.0, 'haleness': 1.0, 'brute_intensity': 0},
    'Automaton': {'brute_intensity': 15, 'brute_resistance': 5.0, 'nimbleness': 2.0, 'haleness': 4.0,
                  'star_intensity': -3.0, 'moon_intensity': -3.0, 'void_intensity': -3.0}
}

CLASS_DATA = {
    'Wandering Spellsword': {
        'bonus_stats': ['melee_damage', 'moon_intensity', 'diplomacy'],
        'stat_mods': {'melee_damage': 3.0, 'moon_intensity': 3.0, 'diplomacy': 2.0, 'brute_intensity': 5},
        'default_cards': []
    },
    'Student': {
        'bonus_stats': ['star_intensity', 'moon_intensity', 'void_intensity'],
        'stat_mods': {'star_intensity': 2.0, 'moon_intensity': 2.0, 'void_intensity': 2.0},
        'default_cards': [],
        'req_card': ['Training']
    },
    'Day Mage': {
        'bonus_stats': ['star_intensity', 'moon_resistance', 'void_vulnerability'],
        'stat_mods': {'star_intensity': 4.0, 'moon_resistance': 3.0, 'void_vulnerability': 1.0},
        'default_cards': [],
        'req_class': ['Student'],
        'req_card': ['Singe'],
        'req_level': 4,
    },
    'Night Mage': {
        'bonus_stats': ['moon_intensity', 'void_resistance', 'star_vulnerability'],
        'stat_mods': {'moon_intensity': 4.0, 'void_resistance': 3.0, 'star_vulnerability': 1.0},
        'default_cards': [],
        'req_class': ['Student'],
        'req_card': ['Wax', 'Wain'],
        'req_level': 4,
    },
    'Passage Mage': {
        'bonus_stats': ['void_intensity', 'star_resistance', 'moon_vulnerability'],
        'stat_mods': {'void_intensity': 4.0, 'star_resistance': 3.0, 'moon_vulnerability': 1.0},
        'default_cards': [],
        'req_class': ['Student'],
        'req_card': ['Chill'],
        'req_level': 4,
    },
    'Warlock': {
        'bonus_stats': ['void_intensity', 'star_resistance', 'melee_resistance', 'moon_vulnerability'],
        'stat_mods': {'void_intensity': 4.0, 'star_resistance': 3.0, 'melee_resistance': 2.0},
        'default_cards': ['Cursed Readings']
    },
    'Scout': {
        'bonus_stats': ['ranged_damage', 'survival_intensity', 'melee_resistance', 'moon_resistance'],
        'stat_mods': {'ranged_damage': 3.0, 'survival_intensity': 3.0, 'melee_resistance': 2.0},
        'default_cards': ['Archery', 'First Aid'],
        'req_card': ['Simple Trap']
    },
    'Ranger': {
        'bonus_stats': ['ranged_damage', 'survival_intensity', 'melee_resistance', 'moon_resistance'],
        'stat_mods': {'ranged_damage': 4.0, 'survival_intensity': 4.0, 'melee_resistance': 2.0},
        'default_cards': ['First Aid'],
        'req_class': ['Scout'],
        'req_card': ['Honed Archery'],
    },
    'Blackcloak': {
        'bonus_stats': ['moon_intensity', 'survival_intensity', 'melee_resistance', 'void_resistance'],
        'stat_mods': {'moon_intensity': 3.0, 'survival_intensity': 3.0, 'melee_resistance': 2.0},
        'default_cards': [],
        'req_class': ['Scout'],
        'req_card': ['Wax'],
        'req_level': 6,
    },
    'Squire': {
        'bonus_stats': ['melee_damage', 'melee_resistance', 'star_vulnerability', 'moon_vulnerability'],
        'stat_mods': {'melee_damage': 3.0, 'melee_resistance': 3.0},
        'default_cards': []
    },
    'Knight': {
        'bonus_stats': ['melee_damage', 'melee_resistance', 'ranged_resistance', 'star_vulnerability'],
        'stat_mods': {'melee_damage': 4.0, 'melee_resistance': 4.0},
        'default_cards': [],
        'req_class': ['Squire'],
        'req_card': ['Honed Slash'],
    },
    'Paladin': {
        'bonus_stats': ['melee_damage', 'star_intensity', 'melee_resistance', 'moon_resistance'],
        'stat_mods': {'melee_damage': 4.0, 'star_intensity': 3.0, 'melee_resistance': 3.0},
        'default_cards': ['Burning Blade']
    },

    # Enemy specific classes
    'Husk': {
        'bonus_stats': ['ranged_damage', 'star_vulnerability'],
        'stat_mods': {'brute_intensity' : -2, 'brute_resistance': -1, 'nimbleness': -3, 'haleness': -5.0,},
        'default_cards': ['Slash', 'Heavy Slash']
    },
    'Soul': {
        'bonus_stats': ['void_intensity', 'moon_vulnerability'],
        'stat_mods': {'brute_intensity' : -4, 'brute_resistance': -1, 'nimbleness': -3, 'haleness': -8.0, 'void_intensity': 2, 'moon_vulnerability': 5},
        'default_cards': ['Light Slash', 'Chill', 'Chill Breath']
    },
    'Rotmonger': {
        'bonus_stats': ['moon_intensity', 'star_vulnerability'],
        'stat_mods': {'brute_intensity' : 0, 'brute_resistance': 3, 'nimbleness': -9, 'haleness': 3.0, 'moon_intensity': 3, 'star_vulnerability': 3},
        'default_cards': ['Heavy Slash', 'Wax']
    }
}


# --- CARDS DATABASE ---

CARD_DATA = [
    {
        'name': 'Wait',
        'type': 'nothingness',
        'rarity': '',
        'target': 'self',
        'recovery_cost': 5,
        'description': 'Do nothing just yet.',
        'stat_boosts': {},
        'is_consumable': False,
        'is_wait': True,
        'illust': """
+                 +
    \  \ |   /     
        \          
    -    X    -    
        /          
    /    |   \     
+                 +
"""
    },
    {
        'name': 'Wallow',
        'type': 'nothingness',
        'rarity': '',
        'target': 'self',
        'recovery_cost': 6,
        'description': 'You should have been more prepared! Do nothing.',
        'stat_boosts': {},
        'illust': """
+                 +
    \  \ |   /     
        \          
    -    X    -    
        /          
    /    |   \     
+                 +
"""
    },
    {
        'name': 'Potion',
        'type': 'trinket',
        'rarity': 'mundane',
        'target': 'ally',
        'recovery_cost': 15,
        'heal_power': 6.0,
        'give_heal_power': 6.0,
        'description': 'Heals an ally. Consumed on use.',
        'stat_boosts': {},
        'is_consumable': True,
        'illust': """
+------\---/------+
|      |   |      |
|     / *   \     |
|    | o * * |    |
|    |   * o |    |
|     \_____/     |
+-----------------+
"""
    },
    {
        'name': 'Sour Potion',
        'type': 'trinket',
        'rarity': 'mundane',
        'target': 'ally',
        'recovery_cost': 1,
        'heal_power': 3.0,
        'give_heal_power': 3.0,
        'description': 'Rapidly heals an ally. Consumed on use.',
        'stat_boosts': {},
        'is_consumable': True,
        'illust': """
+------\~~~/------+
|      | . |      |
|     / * . \     |
|    | o.*.* |    |
|    |. .* o |    |
|     \_____/     |
+-----------------+
"""
    },
    {
        'name': 'Syrupy Potion',
        'type': 'trinket',
        'rarity': 'mundane',
        'target': 'ally',
        'recovery_cost': 30,
        'heal_power': 30.0,
        'give_heal_power': 30.0,
        'description': 'Slugishly heals an ally. Consumed on use.',
        'stat_boosts': {},
        'is_consumable': True,
        'illust': """
+------\-~-/------+
|      || ||      |
|     //0  )\     |
|    ||o O .||    |
|    ||  . o||    |
|     \(___//     |
+-----------------+
"""
    },
    {
        'name': 'Slash',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'melee_damage',
        'damage_power': 2.0,
        'description': 'Standard attack.',
        'stat_boosts': {'melee_damage': 0.2},
        'illust': """
+-----------------+
|     - -   _.    |
|      - - / |    |
|    -  . ///     |
|        \//      |
|       //\.      |
+-------*---------+
"""
    },
    {
        'name': 'Heavy Slash',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 20,
        'damage_type': 'melee_damage',
        'damage_power': 3.0,
        'description': 'Standard attack.',
        'stat_boosts': {'melee_damage': 0.2},
        'illust': """
+-----------------+
|     - -   _.    |
|      - - / |    |
|    -  . ///     |
|        \//      |
|       //\.      |
+-------*---------+
"""
    },
    {
        'name': 'Light Slash',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 5,
        'damage_type': 'melee_damage',
        'damage_power': 1.0,
        'description': 'Standard attack.',
        'stat_boosts': {'melee_damage': 0.2},
        'illust': """
+-----------------+
|     - -   _.    |
|      - - / |    |
|    -  . ///     |
|        \//      |
|       //\.      |
+-------*---------+
"""
    },
    {
        'name': 'Light Clothes',
        'type': 'armor',
        'rarity': 'mundane',
        'target': 'ally',
        'recovery_cost': 5,
        'description': 'Protective garments.',
        'stat_boosts': {'brute_resistance': 0.15, 'melee_resistance': 0.3, 'ranged_resistance': 0.3}
    },
    {
        'name': 'Archery',
        'type': 'weapon',
        'rarity': 'mundane',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'ranged_damage',
        'damage_power': 2.0,
        'description': 'Standard attack.',
        'stat_boosts': {'ranged_damage': 0.2, 'nimbleness': 0.2},
        'illust': """
+-----------------+
|                 |
|   >>======>     |
|                 |
|       >>======> |
|                 |
+-----------------+
"""
    },
    {
        'name': 'Simple Trap',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 5,
        'damage_type': 'survival_intensity',
        'damage_power': 1.0,
        'description': 'A scout\'s cleaver attack.',
        'stat_boosts': {'survival_intensity': 0.2, 'ranged_damage': 0.2, 'nimbleness': 0.2},
        'illust': """
+-----------------+
|                 |
|                 |
|                 |
|                 |
|                 |
+-----------------+
"""
    },
    {
        'name': 'First Aid',
        'type': 'trinket',
        'rarity': 'interesting',
        'target': 'ally',
        'recovery_cost': 10,
        'heal_power': 1.0,
        'heal_stat': 'survival_intensity',
        'description': 'Heals an ally.',
        'stat_boosts': {'survival_intensity': 0.3, 'haleness': 0.2}
    },
    {
        'name': 'Wain',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'moon_intensity',
        'damage_power': 1.0,
        'description': 'Magic spell dealing damage.',
        'stat_boosts': {'moon_intensity': 0.2, 'moon_resistance': 0.3, 'star_vulnerability': 0.3},
        'illust': """
+-----------------+
| *       \  O \  |
|         | o  |' |
|         /  0 /  |
|        _/'.//   |
|      ./_//'    *|
+-----------------+
"""
    },
    {
        'name': 'Wax',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'ally',
        'recovery_cost': 10,
        'heal_power': 1.0,
        'heal_stat': 'moon_intensity',
        'description': 'Magic spell healing an ally.',
        'stat_boosts': {'moon_intensity': 0.2, 'moon_resistance': 0.3, 'star_vulnerability': 0.3},
        'illust': """
+-----------------+
| *       \  O \  |
|         | o  |' |
|         /  0 /  |
|        _/'.//   |
|      ./_//'    *|
+-----------------+
"""
    },
    {
        'name': 'Pull of Tides',
        'type': 'scroll',
        'rarity': 'odd',
        'target': 'all_enemies',
        'recovery_cost': 25,
        'damage_type': 'moon_intensity',
        'damage_power': 2.0,
        'description': 'Magic spell dealing damage to all enemies.',
        'stat_boosts': {'moon_intensity': 0.4, 'moon_resistance': 0.3, 'star_vulnerability': 0.3},
        'illust': """
+-----------------+
| ~  ~     ~    ~ |
|@@~ ~@~@~  ~@@~  |
|uu@~@uuu@~~@uu@@~|
| ~uuu~ ~uuuu~ uuu|
|    .    .    .  |
+-----------------+
"""
    },
    {
        'name': 'Singe',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 12,
        'damage_type': 'star_intensity',
        'damage_power': 2.0,
        'description': 'Magic spell dealing damage.',
        'stat_boosts': {'star_intensity': 0.2, 'star_resistance': 0.3, 'void_vulnerability': 0.3}
    },
    {
        'name': 'Singe Breath',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'all_enemies',
        'recovery_cost': 12,
        'damage_type': 'star_intensity',
        'damage_power': 1,
        'description': 'Magic spell dealing damage to all enemies.',
        'stat_boosts': {'star_intensity': 0.2, 'star_resistance': 0.3, 'void_vulnerability': 0.3}
    },
    {
        'name': 'Chill',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 10,
        'damage_type': 'void_intensity',
        'damage_power': 2.0,
        'description': 'Magic spell dealing damage.',
        'stat_boosts': {'void_intensity': 0.2, 'void_resistance': 0.3, 'moon_vulnerability': 0.3},
        'illust': """
+-----------------+
| ~~~~~ ~~~~~ ~~~ |
|  ~~~~~~~~~~~~~  |
| ~~~ ~~~~~ ~~~~~ |
|~~~~~~~~~~~~~~~~~|
|#################|
+-----------------+
"""
    },
    {
        'name': 'Chill Breath',
        'type': 'scroll',
        'rarity': 'interesting',
        'target': 'all_enemies',
        'recovery_cost': 12,
        'damage_type': 'void_intensity',
        'damage_power': 1.0,
        'description': 'Magic spell dealing damage to all enemies.',
        'stat_boosts': {'void_intensity': 0.2, 'void_resistance': 0.3, 'moon_vulnerability': 0.3},
        'illust': """
+-----------------+
| ~~~~~ ~~~~~ ~~~ |
|  ~~~~~~~~~~~~~  |
| ~~~ ~~~~~ ~~~~~ |
|~~~~~~~~~~~~~~~~~|
|#################|
+-----------------+
"""
    },
    {
        'name': 'Study',
        'type': 'trinket',
        'rarity': 'interesting',
        'target': 'self',
        'recovery_cost': 8,
        'description': 'Focuses mind, boosting magic stats.',
        'stat_boosts': {'star_intensity': 0.2, 'moon_intensity': 0.2, 'void_intensity': 0.2}
    },
    {
        'name': 'Training',
        'type': 'trinket',
        'rarity': 'interesting',
        'target': 'self',
        'recovery_cost': 8,
        'description': 'Physical training, boosting physical stats.',
        'stat_boosts': {'brute_intensity': 0.2, 'brute_resistance': 0.2, 'nimbleness': 0.1}
    },
    {
        'name': 'Honed Archery',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 14,
        'damage_type': 'ranged_damage',
        'damage_power': 3,
        'description': 'Precise attack.',
        'stat_boosts': {'ranged_damage': 0.5},
        'illust': """
+-----------------+
|               >>=
|   >>======>     |
=>                |
|       >>======> |
|                 |
+-----------------+
"""
    },
    {
        'name': 'Honed Slash',
        'type': 'weapon',
        'rarity': 'interesting',
        'target': 'enemy',
        'recovery_cost': 14,
        'damage_type': 'melee_damage',
        'damage_power': 3,
        'description': 'Powerful attack.',
        'stat_boosts': {'melee_damage': 0.5},
        'illust': """
+-----------------+
\     - -   _.    |
\      - - / |    |
|    -  . ///     \\
|        \//      \\
|       //\.      |
+-----------------+
"""
    },
    {
        'name': 'Burning Blade',
        'type': 'weapon',
        'rarity': 'odd',
        'target': 'enemy',
        'recovery_cost': 12,
        'damage_type': 'melee_damage',
        'damage_power': 3,
        'description': 'Flaming melee strike dealing damage.',
        'stat_boosts': {'melee_damage': 0.5, 'star_intensity': 0.5}
    },
    {
        'name': 'Cursed Readings',
        'type': 'scroll',
        'rarity': 'odd',
        'target': 'enemy',
        'recovery_cost': 12,
        'damage_type': 'void_intensity',
        'damage_power': 3,
        'description': 'Dark void incantation dealing damage.',
        'stat_boosts': {'void_intensity': 0.8}
    },
    {
        'name': 'Scorch',
        'type': 'scroll',
        'rarity': 'exceptional',
        'target': 'enemy',
        'recovery_cost': 12,
        'damage_type': 'star_intensity',
        'damage_power': 3,
        'description': 'Day Mage signature spell searing enemies.',
        'stat_boosts': {'star_intensity': 0.6}
    },
    {
        'name': 'Moonlight',
        'type': 'scroll',
        'rarity': 'exceptional',
        'target': 'all_allies',
        'recovery_cost': 12,
        'heal_power': 4.0,
        'heal_stat': 'moon_intensity',
        'description': 'Bathes allies in healing moonlight.',
        'stat_boosts': {'moon_intensity': 0.6, 'moon_resistance': 0.6}
    },
    {
        'name': 'Call to the Void',
        'type': 'scroll',
        'rarity': 'exceptional',
        'target': 'all_enemies',
        'recovery_cost': 14,
        'damage_type': 'void_intensity',
        'damage_power': 1.2,
        'description': 'Strikes all enemies with void energy.',
        'stat_boosts': {'void_intensity': 0.8}
    }
]

CARDS = { card.get('name','') : card for card in CARD_DATA }


# --- CHARACTER MODEL ---

class Character:
    def __init__(self, char_id=None, name="Traveler", species="Fox", current_class="Wandering Spellsword", level=1, level_up_cards=None):
        self.id = char_id or str(uuid.uuid4())[:8]
        self.name = name
        self.species = species if species in SPECIES_DATA else "Fox"
        self.current_class = current_class if current_class in CLASS_DATA else "Wandering Spellsword"
        
        if level_up_cards is not None:
            self.level_up_cards = list(level_up_cards)
        elif level > 1:
            needed_cards = (level * level + level) // 2 - 1
            self.level_up_cards = ['Slash'] * needed_cards
        else:
            self.level_up_cards = []
        
        # Calculate max hp & current hp based on stats
        scaled_stats = self.get_scaled_stats()
        haleness = scaled_stats.get('haleness', 2)
        self.update_max_hp()
        self.current_hp = self.max_hp
        self.action_timer = 0
        self.equipped_cards = []  # Specific equipped cards

    @property
    def level(self):
        """Returns scaled level (0-20) derived from raw level stat using raw_to_scaled."""
        return self.get_scaled_stats().get('level', 1)

    def get_accessible_stats(self):
        """Returns the list of stats this character currently has access to."""
        class_info = CLASS_DATA.get(self.current_class, {})
        bonus = class_info.get('bonus_stats', [])
        return CORE_STATS + bonus

    def get_raw_stats(self):
        """Calculates raw base stats: (base + species + class) * (1 + card_bonuses).
        Every card in level_up_cards contributes 1 to raw level value.
        """
        raw = {stat: 1.0 for stat in ALL_STATS}
        raw['level'] = 2
        
        # Apply species mods
        sp_mods = SPECIES_DATA.get(self.species, {})
        for k, v in sp_mods.items():
            raw[k] = raw.get(k, 1.0) + v

        # Apply class mods
        cl_info = CLASS_DATA.get(self.current_class, {})
        cl_mods = cl_info.get('stat_mods', {})
        for k, v in cl_mods.items():
            raw[k] = raw.get(k, 1.0) + v

        # Apply card bonuses from leveling history
        card_bonuses = {}
        for card_name in self.level_up_cards:
            card = CARDS.get(card_name, {})
            boosts = card.get('stat_boosts', {})
            for k in ALL_STATS:
                default_bonus = 0.1
                if k == 'brute_intensity':
                    default_bonus = 0.0
                elif k == 'level':
                    default_bonus = 0.2
                card_bonuses[k] = card_bonuses.get(k, 0) + boosts.get(k, default_bonus)

        for k, b in card_bonuses.items():
            if k in raw:
                raw[k] = raw[k] * (1.0 + b)

        return raw

    def get_scaled_stats(self):
        """Returns integer 0-20 scaled stats for accessible stats."""
        raw = self.get_raw_stats()
        accessible = self.get_accessible_stats()
        scaled = {}
        for stat in accessible:
            scaled[stat] = raw_to_scaled(raw.get(stat, 0.0))
        return scaled

    def get_combat_scaled_stat(self, damage_stat_name, stat = ""):
        """A ulity of getting the value we should use for a stat mid-combat"""

        scaled_stats = self.get_scaled_stats()
        stat_name = damage_stat_name
        
        if stat:
            stat_name = stat_name.replace('intensity', stat).replace('damage', stat)

        if stat_name in scaled_stats:
            return scaled_stats[stat_name]
        elif stat_name in MAGIC_STATS:
            return 0
        elif stat in damage_stat_name and 'brute_intensity' in scaled_stats:
            return scaled_stats['brute_intensity']
        elif "resistance" in damage_stat_name and 'brute_resistance' in scaled_stats:
            return scaled_stats['brute_resistance']
        else:
            return 0

    def get_stat_xps(self):
        raw = self.get_raw_stats()
        scaled = self.get_scaled_stats() 

        xps = {}
        for k, stat in scaled.items():
            xps[k] = (raw[k] - scaled_to_raw(stat)) / (scaled_to_raw(stat + 1) - scaled_to_raw(stat))

        return xps

    def get_known_cards(self):
        """Returns move cards granted by current class plus equipped cards."""
        cl_info = CLASS_DATA.get(self.current_class, {})
        default_cards = list(cl_info.get('default_cards', []))
        return default_cards + self.equipped_cards

    def give_card(self, card_name):
        """Gives a card to character to boost stats and raw level."""
        if self.level >= 20:
            return False, "Character is already at maximum level."
        if card_name not in CARDS:
            return False, f"Unknown card '{card_name}'."
        
        card = CARDS[card_name]
        if card.get('rarity') == 'mundane':
            # Interesting cards give stats but cannot be learned directly as equipped moves
            pass
        else:
            can_equip = True
            replaced_card_name = None
            for equipped_card_name in self.equipped_cards:
                equipped_card = CARDS[equipped_card_name]
                if card.get('type') == equipped_card.get('type'):
                    if equipped_card.get('rarity') == 'peerless':
                        can_equip = False
                    elif RARITIES.index(equipped_card.get('rarity')) > RARITIES.index(card.get('rarity')):
                        can_equip = False
                    else:
                        replaced_card_name = equipped_card_name

            if can_equip:
                if replaced_card_name:
                    self.equipped_cards.remove(replaced_card_name)
                self.equipped_cards.append(card_name)

        self.level_up_cards.append(card_name)

        # Re-evaluate class
        self.update_class()

        # Re-evaluate max HP
        old_max = self.max_hp
        self.update_max_hp()
        self.current_hp = min(self.max_hp, self.current_hp + (self.max_hp - old_max))

        self.current_hp = min(self.max_hp, self.current_hp + int(card.get('give_heal_power', 0)))

        return True, f"Gave {card_name} to {self.name}! Level is now {self.level}."

    def update_class(self):
        for class_name in CLASS_DATA:
            if class_name != self.current_class:
                cl = CLASS_DATA[class_name]
                has_class_req = 'req_class' in cl
                has_card_req = 'req_card' in cl
                has_level_req = 'req_level' in cl
                has_species_req = 'req_species' in cl

                if not has_class_req and not has_card_req and not has_level_req and not has_species_req:
                    continue

                class_req = not has_class_req or self.current_class in cl.get('req_class')
                card_req = not has_card_req or any(c in self.equipped_cards for c in cl.get('req_card'))
                level_req = not has_level_req or self.get_scaled_stats()['level'] >= cl.get('req_level')
                species_req = not has_species_req or self.species in cl.get('req_species')

                if class_req and card_req and level_req and species_req:
                    self.current_class = class_name

    def update_max_hp(self): 
        scaled_stats = self.get_scaled_stats()
        self.max_hp = max(2, 10 + scaled_stats.get('haleness', 2) * 2)

    def is_alive(self):
        return self.current_hp > 0

    def illust(self):
        for illust in ILLUSTRATION_DATA:
            species_match = 'species' not in illust or self.species in illust['species']
            class_match = 'classes' not in illust or self.current_class in illust['classes']
            if species_match and class_match:
                return 'game/{0}.png'.format(illust.get('name',''))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'species': self.species,
            'current_class': self.current_class,
            'level_up_cards': self.level_up_cards,
            'current_hp': self.current_hp,
            'max_hp': self.max_hp,
            'action_timer': self.action_timer,
            'equipped_cards': self.equipped_cards
        }

    @classmethod
    def from_dict(cls, d):
        cards = d.get('level_up_cards', None)
        c = cls(
            char_id=d.get('id'),
            name=d.get('name', 'Traveler'),
            species=d.get('species', 'Fox'),
            current_class=d.get('current_class', 'Wandering Spellsword'),
            level_up_cards=cards
        )
        c.equipped_cards = d.get('equipped_cards', [])
        # Recalculate max_hp based on state
        scaled_stats = c.get_scaled_stats()
        c.update_max_hp()
        c.current_hp = d.get('current_hp', c.max_hp)
        c.action_timer = d.get('action_timer', 0)
        return c


# --- PARTY & OVERWORLD MAP ---

class Party:
    def __init__(self):
        self.members = []
        self.inventory = []  # list of card names (up to 20)
        self.shared_deck = []  # list of card names (up to 10)
        self.gold = 50
        self.x = 7
        self.y = 5

    def to_dict(self):
        return {
            'members': [m.to_dict() for m in self.members],
            'inventory': self.inventory,
            'shared_deck': self.shared_deck,
            'gold': self.gold,
            'x': self.x,
            'y': self.y
        }

    @classmethod
    def from_dict(cls, d):
        p = cls()
        p.members = [Character.from_dict(m) for m in d.get('members', [])]
        p.inventory = d.get('inventory', [])
        p.shared_deck = d.get('shared_deck', [])
        p.gold = d.get('gold', 50)
        p.x = d.get('x', 7)
        p.y = d.get('y', 5)
        return p


# --- COMBAT ENGINE ---

class CombatEngine:
    def __init__(self, allies, enemies, shared_deck = []):
        self.allies = allies  # List of Character objects
        self.enemies = enemies  # List of Character objects (built using Character class!)
        self.shared_deck = shared_deck
        self.combat_log = []
        self.is_over = False
        self.victory = False

    def start_combat(self):
        # Reset action timers
        for c in self.allies + self.enemies:
            c.action_timer = 20 - c.get_scaled_stats().get("nimbleness", 0)

        # Build party shared deck
        deck_pool = list(self.shared_deck)
        while len(deck_pool) < DECK_MINIMUM_SIZE:
            deck_pool.append("Wallow")
        for a in self.allies:
            deck_pool.extend(a.get_known_cards())
        random.shuffle(deck_pool)
        self.draw_pile = deck_pool
        self.discard_pile = []
        self.hand = []
        self.draw_hand()

    def draw_hand(self):
        """Draws up to 3 cards for the player turn hand."""

        # Do not draw cards once the combat is over
        if self.is_over:
            return

        needed = 3 - len(self.hand)
        for _ in range(needed):
            if not self.draw_pile:
                if self.discard_pile:
                    self.draw_pile = self.discard_pile
                    self.discard_pile = []
                    random.shuffle(self.draw_pile)
                else:
                    break
            if self.draw_pile:
                self.hand.append(self.draw_pile.pop(0))

    def get_current_turn_character(self):
        """Returns the character with the lowest action timer."""
        active = [c for c in self.allies + self.enemies if c.is_alive()]
        if not active:
            return None
        active.sort(key=lambda c: c.action_timer)
        return active[0]

    def advance_turn_timers(self):
        """Fast-forwards action timers until a living character reaches turn execution."""
        turn_char = self.get_current_turn_character()
        if not turn_char:
            return None
        min_timer = turn_char.action_timer
        if min_timer > 0:
            for c in self.allies + self.enemies:
                if c.is_alive():
                    c.action_timer = max(0, c.action_timer - min_timer)

        print(f"[Combat!] Start of turn: {', '.join([f'{c.name}: {c.action_timer} ticks' for c in self.allies + self.enemies])}")
        return turn_char

    def execute_enemy_turn(self, enemy):
        """AI execution for an enemy character turn."""
        living_allies = [a for a in self.allies if a.is_alive()]
        living_enemies = [e for e in self.enemies if e.is_alive()]
        damaged_enemies = [e for e in living_enemies if e.current_hp < e.max_hp]
        if not living_allies:
            return

        known = enemy.get_known_cards()
        card_name = random.choice(known) if known else 'Slash'
        card = CARDS.get(card_name, CARDS['Slash'])

        target = random.choice(living_allies)
        if card.get('target') == 'ally':
            if card.get('heal_power') > 0 and damaged_enemies:
                target = random.choice(damaged_enemies)
            else:
                target = random.choice(living_enemies)

        self.apply_card_effect(enemy, card, target)
        
        # Increase action timer
        stats = enemy.get_scaled_stats()
        nimble = stats.get('nimbleness', 0)
        # 4* ... /4 messes with the round, to help nimbleness stats not divisible by 4
        rec = ((4 * card.get('recovery_cost', 10)) - nimble) / 4
        enemy.action_timer += int(round(rec))

    def apply_card_effect(self, actor, card, target):
        """Calculates and applies card damage or healing."""
        actor_stats = actor.get_scaled_stats()
        card_name = card['name']

        if card.get('is_wait'):
            self.combat_log.append(f"{actor.name} waited to recover energy.")

        if 'heal_power' in card:
            heal_stat_name = card.get('heal_stat', '')
            heal_amount = int(card['heal_power'])
            if heal_stat_name:
                heal_stat = actor_stats.get(heal_stat_name, actor_stats.get('brute_intensity', 2))
                heal_amount = int(round(heal_amount * heal_stat))
            
            if card.get('target') in ['all_allies', 'all_enemies']:
                targets = self.allies if actor in self.allies else self.enemies
            else:
                targets = [target] if target else [actor]

            for t in targets:
                if t and t.is_alive():
                    t.current_hp = min(t.max_hp, t.current_hp + heal_amount)
                    self.combat_log.append(f"{actor.name} used {card_name} on {t.name}, healing {heal_amount} HP!")

        # Damage calculation
        if 'damage_power' in card:
            dmg_type = card.get('damage_type', 'melee_damage')
            base_power = card.get('damage_power')

            # Attacker stat
            atk_val = actor.get_combat_scaled_stat(dmg_type)

            targets = []
            if card.get('target') in ['all_enemies', 'all_allies']:
                targets = [e for e in (self.enemies if actor in self.allies else self.allies) if e.is_alive()]
            elif target:
                targets = [target]

            for t in targets:
                if not t or not t.is_alive():
                    continue

                # Resistance stat
                res_val = t.get_combat_scaled_stat(dmg_type, "resistance")
                vul_val = t.get_combat_scaled_stat(dmg_type, "vulnerability")

                raw_dmg = (base_power * atk_val) + vul_val - res_val
                print(f"[Combat!] Damage calc for {card_name}: base_power: {base_power}, atk_val: {atk_val}, vul_val: {vul_val}, res_val: {res_val} => {raw_dmg}")

                dmg = max(1, int(round(raw_dmg)))
                t.current_hp = max(0, t.current_hp - dmg)
                self.combat_log.append(f"{actor.name} used {card_name} on {t.name} for {dmg} damage!")

        print(f"[Combat!] Turn complete: {', '.join([f'{c.name}: {c.action_timer} ticks' for c in self.allies + self.enemies])}")

    def execute_player_turn(self, actor, card_name, target_id):
        """Processes player character turn using card_name and target_id."""
        self.combat_log = []
        if card_name == 'Wait':
            card = CARDS['Wait']
            target = actor
        else:
            if card_name in self.hand:
                self.hand.remove(card_name)
                self.discard_pile.append(card_name)
            card = CARDS.get(card_name, CARDS['Slash'])
            
            # Find target
            all_chars = self.allies + self.enemies
            target = next((c for c in all_chars if c.id == target_id), None)

        self.apply_card_effect(actor, card, target)

        # Increase action timer
        stats = actor.get_scaled_stats()
        nimble = stats.get('nimbleness', 2)
        rec = ((4 * card.get('recovery_cost', 10)) - nimble) / 4
        actor.action_timer += int(round(rec))

        # Replenish hand
        self.draw_hand()

    def check_combat_end(self):
        """Checks victory or loss conditions."""
        allies_alive = any(a.is_alive() for a in self.allies)
        enemies_alive = any(e.is_alive() for e in self.enemies)

        if not enemies_alive:
            self.is_over = True
            self.victory = True
            self.combat_log.append("> Victory! All enemies were defeated! Take a momment to catch your breath, and venture on.")
            return True
        elif not allies_alive:
            self.is_over = True
            self.victory = False
            self.combat_log.append("> Defeat! All party members were downed.")
            return True
        return False

    def to_dict(self):
        return {
            'allies': [a.to_dict() for a in self.allies],
            'enemies': [e.to_dict() for e in self.enemies],
            'shared_deck': self.shared_deck,
            'combat_log': self.combat_log,
            'is_over': self.is_over,
            'victory': self.victory,
            'draw_pile': self.draw_pile,
            'discard_pile': self.discard_pile,
            'hand': self.hand
        }

    @classmethod
    def from_dict(cls, d):
        allies = [Character.from_dict(a) for a in d.get('allies', [])]
        enemies = [Character.from_dict(e) for e in d.get('enemies', [])]
        engine = cls(allies, enemies, d.get('shared_deck', []))
        engine.combat_log = d.get('combat_log', [])
        engine.is_over = d.get('is_over', False)
        engine.victory = d.get('victory', False)
        engine.draw_pile = d.get('draw_pile', [])
        engine.discard_pile = d.get('discard_pile', [])
        engine.hand = d.get('hand', [])
        return engine


# --- HELPER: INITIAL GAME STATE CREATION ---

def create_initial_game_state():
    """Initializes standard starting game state per gdd.txt."""
    # Starting character: 1 Level 1 Fox Wandering Spellsword
    hero = Character(name="Yew", species="Fox", current_class="Wandering Spellsword")
    
    party = Party()
    party.members.append(hero)
    
    # Starting cards per GDD: 5 health potions, 6 slashes, 3 light clothes
    starting_inventory = (
        ['Potion'] * 4 +
        ['Wain'] * 1
    )
    party.inventory = starting_inventory
    party.shared_deck = ( 
        ['Slash'] * 5 +
        ['Light Slash', 'Heavy Slash'] +
        ['Potion'] * 2 +
        ['Wain'] * 1
    )

    return {
        'screen': 'voinara_intro',  # Start at Voinara dialogue screen
        'voinara_step': 0,
        'party': party.to_dict(),
        'active_menu': None,  # None, 'character_menu', 'shop', 'inn', 'combat'
        'combat': None,
        'message': "Welcome to Legs on Strange Lands."
    }

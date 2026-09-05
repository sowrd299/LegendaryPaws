import math
import random
import uuid
from .illustration import ILLUSTRATION_DATA
from .cards import *
from .templatetags.utils import stat_name

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
    'Ember Sprite': {'star_intensity': 5.0, 'star_resistance': 4.0, 'haleness': 1.0, 'brute_intensity': 0},
    'Dew Sprite': {'moon_intensity': 5.0, 'moon_resistance': 4.0, 'haleness': 1.0, 'brute_intensity': 0},
    'Loss Sprite': {'void_intensity': 3.0, 'void_resistance': 4.0, 'haleness': 0.0, 'brute_intensity': 0, 'nimbleness': 3.0},
    'Clockwork': {'brute_intensity': 15, 'brute_resistance': 5.0, 'nimbleness': 2.0, 'haleness': 4.0,
                  'star_intensity': -3.0, 'moon_intensity': -3.0, 'void_intensity': -3.0},

    # Enemy specific species
    'Giant': {'brute_intensity': 15, 'brute_resistance': 15.0, 'haleness': 8.0},
    'Dragon': {'brute_intensity': 25, 'brute_resistance': 15.0, 'haleness': 25.0, 'nimbleness': 25},
}

CLASS_DATA = {
    'Wandering Spellsword': {
        'bonus_stats': ['melee_damage', 'moon_intensity', 'diplomacy'],
        'stat_mods': {'melee_damage': 3.0, 'moon_intensity': 3.0, 'diplomacy': 2.0, 'brute_intensity': 5},
        'default_cards': [],
        'req_class': ['Knight'],
        'req_card': ['Wain', 'Wax', 'Waxing Moonlight'],
    },

    # MAGIC CLASSES
    'Student': {
        'bonus_stats': ['star_intensity', 'moon_intensity', 'void_intensity'],
        'stat_mods': {'star_intensity': 2.0, 'moon_intensity': 2.0, 'void_intensity': 2.0},
        'default_cards': [],
        'req_card': ['Elementary Magic', 'Study']
    },
    'Wizard': {
        'bonus_stats': ['star_intensity', 'moon_intensity', 'void_intensity'],
        'stat_mods': {'star_intensity': 3.0, 'moon_intensity': 3.0, 'void_intensity': 3.0},
        'default_cards': ['Magical Opus'],
        'req_class': ['Student'],
        'req_species': ['Owl'],
        'req_level': 3,
    },
    'Day Mage': {
        'bonus_stats': ['star_intensity', 'moon_resistance', 'void_vulnerability'],
        'stat_mods': {'star_intensity': 4.0, 'moon_resistance': 3.0, 'void_vulnerability': 1.0},
        'default_cards': ['Singeing Sunlight'],
        'req_class': ['Student'],
        'req_card': ['Singe', 'Singeing Sunlight'],
        'req_level': 4,
    },
    'Night Mage': {
        'bonus_stats': ['moon_intensity', 'void_resistance', 'star_vulnerability'],
        'stat_mods': {'moon_intensity': 4.0, 'void_resistance': 3.0, 'star_vulnerability': 1.0},
        'default_cards': ['Waxing Moonlight'],
        'req_class': ['Student'],
        'req_card': ['Wax', 'Wain', 'Waxing Moonlight'],
        'req_level': 4,
    },
    'Passage Mage': {
        'bonus_stats': ['void_intensity', 'star_resistance', 'moon_vulnerability'],
        'stat_mods': {'void_intensity': 4.0, 'star_resistance': 3.0, 'moon_vulnerability': 1.0},
        'default_cards': ['Call to the Void'],
        'req_class': ['Student'],
        'req_card': ['Chill', 'Call to the Void'],
        'req_level': 4,
    },
    'Warlock': {
        'bonus_stats': ['void_intensity', 'star_resistance', 'melee_resistance', 'moon_vulnerability'],
        'stat_mods': {'void_intensity': 4.0, 'star_resistance': 3.0, 'melee_resistance': 2.0},
        'default_cards': ['Cursed Readings']
    },

    # SURVIVAL CLASSES
    'Scout': {
        'bonus_stats': ['melee_damage', 'ranged_damage', 'survival_intensity', 'moon_resistance'],
        'stat_mods': {'melee_damage': 3.0, 'ranged_damage': 3.0, 'survival_intensity': 3.0},
        'default_cards': ['Archery', 'First Aid'],
        'req_card': ['Simple Trap']
    },
    'Burglar': {
        'bonus_stats': ['melee_damage', 'survival_intensity', 'moon_resistance'],
        'stat_mods': {'nimbleness': 3, 'melee_damage': 3.0, 'survival_intensity': 3.0},
        'default_cards': ['Backstab'],
        'req_class': ['Scout'],
        'req_species': ['Cat'],
        'req_level': 3,
    },
    'Ranger': {
        'bonus_stats': ['ranged_damage', 'survival_intensity', 'moon_resistance'],
        'stat_mods': {'level': 2, 'ranged_damage': 5.0, 'survival_intensity': 5.0, 'moon_resistance': 1.0},
        'default_cards': ['First Aid'],
        'req_class': ['Scout'],
        'req_level': 6,
    },
    'Blackcloak': {
        'bonus_stats': ['moon_intensity', 'survival_intensity', 'void_resistance'],
        'stat_mods': {'moon_intensity': 3.0, 'survival_intensity': 4.0, 'void_resistance': 2.0},
        'default_cards': ['Cover of Night'],
        'req_class': ['Scout', 'Burglar'],
        'req_card': ['Wain', 'Wax'],
    },
    'Assassin': {
        'bonus_stats': ['melee_damage', 'ranged_damage', 'survival_intensity', 'star_vulnerability'],
        'stat_mods': {'level': 3, 'melee_damage': 6.0, 'ranged_damage': 6.0, 'survival_intensity': 6.0, 'star_vulnerability': 1.0},
        'default_cards': ['Assassinate', 'Snipe'],
        'req_class': ['Ranger', 'Burglar'],
        'req_card': ['Assassinate', 'Snipe'],
    },

    # MELEE CLASSES
    'Squire': {
        'bonus_stats': ['melee_damage', 'melee_resistance', 'star_vulnerability', 'moon_vulnerability'],
        'stat_mods': {'melee_damage': 3.0, 'melee_resistance': 3.0},
        'default_cards': [],
        'req_card': ['Training']
    },
    'Knight': {
        'bonus_stats': ['melee_damage', 'melee_resistance', 'ranged_resistance', 'star_vulnerability'],
        'stat_mods': {'level': 2, 'haleness': 2, 'melee_damage': 5.0, 'melee_resistance': 5.0},
        'default_cards': [],
        'req_class': ['Squire'],
        'req_level': 6,
    },
    'Paladin': {
        'bonus_stats': ['melee_damage', 'star_intensity', 'melee_resistance', 'moon_resistance'],
        'stat_mods': {'melee_damage': 4.0, 'star_intensity': 3.0, 'melee_resistance': 3.0},
        'default_cards': ['Burning Blade']
    },
    'Fencer': {
        'bonus_stats': ['melee_damage', 'nimbleness', 'moon_vulnerability', 'void_vulnerability'],
        'stat_mods': {'melee_damage': 4.0, 'nimbleness': 3.0, 'moon_vulnerability': 2.0, 'void_vulnerability': 2.0},
        'default_cards': ['Parry & Riposte', 'Budding Thrust'],
        'req_card': ['Flowering Stab'],
    },
    'Shieldmate': {
        'bonus_stats': ['void_resistance', 'diplomacy'],
        'stat_mods': {'void_resistance': 15.0, 'brute_resistance': 15.0, 'diplomacy': 2.0},
    },
    'Dragonslayer': {
        'bonus_stats': ['melee_damage', 'void_intensity', 'star_resistance', 'moon_vulnerability'],
        'stat_mods': {'level': 3, 'haleness': 5, 'melee_damage': 5.0, 'void_intensity': 5.0, 'star_resistance': 5.0, 'moon_vulnerability': 3.0},
        'default_cards': [],
        'req_card': ['Dragonsbane'],
    },

    # ====================================================================================================
    # ENEMY CLASSES
    # ====================================================================================================
    
    'Husk': {
        'bonus_stats': ['star_vulnerability'],
        'stat_mods': {'brute_intensity' : -2, 'brute_resistance': -1, 'nimbleness': -3, 'haleness': -5.0, 'star_vulnerability': 1},
        'default_cards': ['Slash', 'Heavy Slash'],
        'playable': False,
    },
    'Hollow': {
        'bonus_stats': ['star_vulnerability'],
        'stat_mods': {'brute_intensity' : 2, 'brute_resistance': 2, 'star_vulnerability': 2, 'haleness': 2},
        'default_cards': ['Slash', 'Heavy Slash'],
        'playable': False,
    },
    'Soul': {
        'bonus_stats': ['void_intensity', 'moon_vulnerability'],
        'stat_mods': {'brute_intensity' : -4, 'brute_resistance': -1, 'nimbleness': -3, 'haleness': -8.0, 'void_intensity': 2, 'moon_vulnerability': 5},
        'default_cards': ['Light Slash', 'Chill', 'Chill Breath'],
        'enemy_species': ['Cat', 'Badger', 'Fox', 'Rabbit', 'Owl'],
        'playable': False,
    },
    'Essence': {
        'bonus_stats': ['void_intensity', 'moon_vulnerability'],
        'stat_mods': {'brute_resistance': 1, 'void_intensity': 5, 'nimbleness': 1, 'moon_vulnerability': 9},
        'default_cards': ['Light Slash', 'Chill', 'Chill Breath', 'Call to the Void'],
        'enemy_species': ['Cat', 'Badger', 'Fox', 'Rabbit', 'Owl'],
        'playable': False,
    },
    'Rotmonger': {
        'bonus_stats': ['moon_intensity', 'star_vulnerability'],
        'stat_mods': {'brute_intensity' : 0, 'brute_resistance': 3, 'nimbleness': -9, 'haleness': 3.0, 'moon_intensity': 3, 'star_vulnerability': 3},
        'default_cards': ['Heavy Slash', 'Wax'],
        'enemy_species': ['Badger', 'Fox', 'Raven'],
        'playable': False,
    },
    'Murmur': {
        'bonus_stats': ['void_intensity', 'melee_resistance', 'ranged_vulnerability'],
        'stat_mods': {'void_intensity': 5, 'melee_resistance': 36, 'ranged_vulnerability': 1},
        'default_cards': ['Chill', 'Chill Breath', 'Step in Shadow'],
        'enemy_species': ['Rabbit', 'Giant'],
        'playable': False,
    },
    'Remnant': {
        'bonus_stats': ['ranged_resistance', 'moon_vulnerability', 'star_vulnerability', 'void_vulnerability'],
        'stat_mods':{'ranged_resistance': 36, 'moon_vulnerability': 1, 'star_vulnerability': 1, 'void_vulnerability': 1},
        'default_cards': ['Shield Spike', 'Slash', 'Heavy Slash', 'Broad Shield'],
        'enemy_species': ['Badger', 'Giant'],
        'playable': False,
    },
    'Blot': {
        'bonus_stats': ['moon_resistance', 'void_resistance', 'star_resistance', 'melee_vulnerability'],
        'stat_mods': {'moon_resistance': 36, 'void_resistance': 36, 'star_resistance': 36, 'melee_vulnerability': 1},
        'default_cards': ['Light Slash', 'Blot the Sky'],
        'enemy_species': ['Fox', 'Giant'],
        'playable': False,
    },

    # ====================================================================================================
    # ENEMY BOSS CLASSES
    # ====================================================================================================

    'Matron': {
        'bonus_stats': ['star_intensity', 'moon_resistance', 'void_vulnerability'],
        'stat_mods': {'star_intensity': 16, 'moon_resistance': 9, 'void_vulnerability': 25},
        'base_hp': 99,
        'default_cards': ['Heavy Slash', 'Rust Breath', 'Mold Breath', 'Heat Breath', 'Shadow Breath']
    }
}


# --- CHARACTER MODEL ---

class Character:
    def __init__(self, char_id=None, name="Traveler", species="Fox", current_class="Wandering Spellsword", level=1, level_up_cards=None):
        self.id = char_id or str(uuid.uuid4())[:8]
        self.name = name
        self.species = species if species in SPECIES_DATA else "Fox"
        self.current_class = current_class if current_class in CLASS_DATA else "Wandering Spellsword"
        self.unlocked_classes = [current_class]
        self.previous_combat_class = None
        self.status_effects = [] # Do this early, since it's checked in get_scaled_stats

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
        self.is_recruited = False

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

        for status_effect in self.status_effects:
            if status_effect.is_active():
                if status_effect.stat not in scaled:
                    scaled[status_effect.stat] = 0
                scaled[status_effect.stat] += status_effect.value

        return scaled

    def get_combat_scaled_stat(self, damage_stat_name, stat = ""):
        """A ulity of getting the value we should use for a stat mid-combat"""

        scaled_stats = self.get_scaled_stats()
        stat_name = damage_stat_name
        
        if stat:
            stat_name = stat_name.replace('intensity', stat).replace('damage', stat)

        brute_stat = 0
        if stat_name in MAGIC_STATS:
            pass # magic stats don't use brute
        elif stat in damage_stat_name and 'brute_intensity' in scaled_stats:
            brute_stat = scaled_stats['brute_intensity']
        elif "resistance" in damage_stat_name and 'brute_resistance' in scaled_stats:
            brute_stat = scaled_stats['brute_resistance']

        if stat_name in scaled_stats:
            return max(scaled_stats[stat_name], brute_stat)
        else:
            return brute_stat

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

    def add_status_effect(self, status_effect):
        self.status_effects.append(status_effect)

    def advance_action_timer(self, amount):
        self.action_timer -= amount

        status_effects_to_remove = []
        for status_effect in self.status_effects:
            status_effect.advance_action_timer(amount)
            if not status_effect.is_active():
                status_effects_to_remove.append(status_effect)

        for status_effect in status_effects_to_remove:
            self.status_effects.remove(status_effect)

    def give_card(self, card_name):
        """Gives a card to character to boost stats and raw level."""
        if self.level >= 20:
            return False, "Character is already at maximum level."
        if card_name not in CARDS:
            return False, f"Unknown card '{card_name}'."
        
        card = CARDS[card_name]

        can_equip, replaced_card_name = self.can_equip_card(card)
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

        if self.is_alive() or card.get('revive'):
            self.current_hp = min(self.max_hp, self.current_hp + (self.max_hp - old_max))
            self.current_hp = min(self.max_hp, self.current_hp + int(card.get('give_heal_power', 0)))

        return True, f"Gave {card_name} to {self.name}! Level is now {self.level}."

    def can_equip_card(self, card): 
        can_equip = True
        replaced_card_name = None

        if card.get('rarity') == 'mundane':
            return False, None

        for equipped_card_name in self.equipped_cards:
            equipped_card = CARDS[equipped_card_name]
            if card.get('type') == equipped_card.get('type'):
                if equipped_card_name == card.get('name', ''):
                    can_equip = False
                elif equipped_card.get('rarity') == 'peerless':
                    can_equip = False
                elif RARITIES.index(equipped_card.get('rarity')) > RARITIES.index(card.get('rarity')):
                    can_equip = False
                else:
                    replaced_card_name = equipped_card_name
        
        return can_equip, replaced_card_name

    def update_class(self):

        new_class = self.current_class

        eligible_classes = []

        for class_name in CLASS_DATA:
            cl = CLASS_DATA[class_name]
            has_class_req = 'req_class' in cl
            has_card_req = 'req_card' in cl
            has_level_req = 'req_level' in cl
            has_species_req = 'req_species' in cl

            if not has_class_req and not has_card_req and not has_level_req and not has_species_req:
                continue

            if not cl.get('playable', True):
                continue

            class_req = not has_class_req or self.previous_combat_class in cl.get('req_class')
            card_req = not has_card_req or any(c in self.equipped_cards for c in cl.get('req_card'))
            level_req = not has_level_req or self.get_scaled_stats().get('level', 1) >= cl.get('req_level')
            species_req = not has_species_req or self.species in cl.get('req_species')

            if (has_class_req and class_req) or (has_card_req and card_req) or  (has_level_req and level_req) or (has_species_req and species_req):
                print(f"[XP!] Considering {self.name} for {class_name}: "
                    f"class_req={class_req}, "
                    f"card_req={card_req}, "
                    f"level_req={level_req}, "
                    f"species_req={species_req}, "
                    f"newly eligible={class_name not in self.unlocked_classes}")

            if class_req and card_req and level_req and species_req:
                eligible_classes.append(class_name)
                
                # the newly eligible class lowest on the list is the new class
                if not class_name in self.unlocked_classes:
                    new_class = class_name
                    self.unlocked_classes.append(class_name)

        self.current_class = new_class

    def update_max_hp(self): 
        scaled_stats = self.get_scaled_stats()
        base_hp = CLASS_DATA.get(self.current_class, {}).get('base_hp', 10)
        self.max_hp = max(2, base_hp + scaled_stats.get('haleness', 0) * 2)

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
            'unlocked_classes': self.unlocked_classes,
            'previous_combat_class': self.previous_combat_class,
            'level_up_cards': self.level_up_cards,
            'current_hp': self.current_hp,
            'max_hp': self.max_hp,
            'action_timer': self.action_timer,
            'equipped_cards': self.equipped_cards,
            'is_recruited': getattr(self, 'is_recruited', False),
            'status_effects': [se.to_dict() for se in self.status_effects]
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
        c.unlocked_classes = d.get('unlocked_classes', [c.current_class])
        c.previous_combat_class = d.get('previous_combat_class', None)
        c.equipped_cards = d.get('equipped_cards', [])
        c.is_recruited = d.get('is_recruited', False)
        # Recalculate max_hp based on state
        scaled_stats = c.get_scaled_stats()
        c.update_max_hp()
        c.current_hp = d.get('current_hp', c.max_hp)
        c.action_timer = d.get('action_timer', 0)
        c.status_effects = [StatusEffect.from_dict(sc) for sc in d.get('status_effects', [])]
        return c


# --- STAT CHANGE ---

class StatusEffect:
    def __init__(self, stat, value, action_timer):
        self.stat = stat
        self.value = value
        self.action_timer = action_timer

    def is_active(self):
        return self.action_timer >= 0

    def advance_action_timer(self, amount):
        self.action_timer -= amount

    def to_dict(self):
        return {
            'stat': self.stat,
            'value': self.value,
            'action_timer': self.action_timer
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d['stat'], d['value'], d['action_timer'])


# --- PARTY & OVERWORLD MAP ---

class Party:
    def __init__(self):
        from .map import DEFAULT_START_INN_ID, get_inn_coords
        start_x, start_y = get_inn_coords(DEFAULT_START_INN_ID)
        self.members = []
        self.inventory = []  # list of card names (up to 20)
        self.shared_deck = []  # list of card names (up to 10)
        self.gold = 50
        self.losable_gold = 0
        self.x = start_x
        self.y = start_y

    def to_dict(self):
        return {
            'members': [m.to_dict() for m in self.members],
            'inventory': self.inventory,
            'shared_deck': self.shared_deck,
            'gold': self.gold,
            'losable_gold': self.losable_gold,
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
        p.losable_gold = d.get('losable_gold', 0)
        p.x = d.get('x', p.x)
        p.y = d.get('y', p.y)
        return p


# --- COMBAT ENGINE ---

class CombatEngine:
    def __init__(self, allies, enemies, shared_deck = [], is_recruitable = False, reward_card = None, reward_gold = 0):
        self.allies = allies  # List of Character objects
        self.enemies = enemies  # List of Character objects (built using Character class!)
        self.shared_deck = shared_deck
        self.is_recruitable = is_recruitable
        self.reward_card = reward_card
        self.reward_gold = reward_gold
        self.combat_log = []
        self.is_over = False
        self.victory = False
        self.draw_pile = []
        self.discard_pile = []
        self.hand = []
        self.draw_reqs = []

    def start_combat(self):
        # Reset action timers
        for c in self.allies + self.enemies:
            c.action_timer = 20 - c.get_scaled_stats().get("nimbleness", 0)

        self.advance_action_timers()

        # Build party shared deck
        self.draw_pile = self.get_deck_pool()
        self.discard_pile = []
        self.hand = []
        self.draw_hand()

    def get_deck_pool(self):
        deck_pool = list(self.shared_deck)
        while len(deck_pool) < DECK_MINIMUM_SIZE:
            deck_pool.append("Wallow")
        for a in self.allies:
            deck_pool.extend(a.get_known_cards())

        for card in getattr(self, 'hand', []):
            if card in deck_pool:
                deck_pool.remove(card)

        return deck_pool

    def draw_hand(self):
        """Draws up to 3 cards for the player turn hand."""

        # Do not draw cards once the combat is over
        if self.is_over:
            return

        def meets_draw_req(card_name, reqs):
            card = CARDS.get(card_name, {})
            return all(card.get(r) == reqs.get(r) for r in reqs)

        needed = 3 - len(self.hand)
        for _ in range(needed):

            draw_req = self.draw_reqs.pop(0) if self.draw_reqs else None

            if not self.draw_pile or (draw_req and not any(meets_draw_req(c, draw_req) for c in self.draw_pile)):
                self.draw_pile = self.get_deck_pool()
                self.discard_pile = []
                random.shuffle(self.draw_pile)
                print(f"[Combat!] Reshuffling deck. {self.draw_pile}")

            if self.draw_pile:
                if draw_req:
                   idx = 0 
                   for i, card_name in enumerate(self.draw_pile):
                       if meets_draw_req(card_name, draw_req):
                           idx = i
                           break
                   self.hand.append(self.draw_pile.pop(idx))
                   random.shuffle(self.draw_pile)
                else:
                   self.hand.append(self.draw_pile.pop(0))

    def get_current_turn_character(self):
        """Returns the character with the lowest action timer."""
        active = self.get_sorted_living_characters()
        return active[0] if active else None

    def get_sorted_living_characters(self):
        """Returns living allies and enemies stably sorted by action_timer."""
        active = [c for c in self.allies + self.enemies if c.is_alive()]
        active.sort(key=lambda c: c.action_timer)
        return active

    def get_hypothetical_turn_info(self, card_name):
        """Calculates projected next turn index and action timer for current turn character if card_name is chosen."""
        turn_char = self.get_current_turn_character()
        if not turn_char:
            return None

        card = CARDS.get(card_name, CARDS.get('Slash', {}))
        stats = turn_char.get_scaled_stats()
        nimble = stats.get('nimbleness', 2)
        rec = int(round(((4 * card.get('recovery_cost', 10)) - nimble) / 4))
        projected_timer = turn_char.action_timer + rec

        active = self.get_sorted_living_characters()
        target_index = 1
        for i in active:
            if i == turn_char:
                continue
            # "Less than" ignores tie breakers, so this isn't actually always right
            if i.action_timer < projected_timer:
                target_index += 1
            else:
                break

        return {
            'target_index': target_index,
            'projected_timer': rec,
            'turn_char': turn_char,
        }


    def advance_action_timers(self):
        """Fast-forwards action timers until a living character reaches turn execution."""
        turn_char = self.get_current_turn_character()
        if not turn_char:
            return None
        min_timer = turn_char.action_timer
        if min_timer > 0:
            for c in self.allies + self.enemies:
                if c.is_alive():
                    c.advance_action_timer(min_timer)

        def get_tick_info_string(character):
            status_effect_string = ', '.join([f'{s.action_timer}' for s in character.status_effects])
            return f'{character.name}: {character.action_timer} ticks ({status_effect_string})'

        print(f"[Combat!] Start of turn: {', '.join([get_tick_info_string(c) for c in self.allies + self.enemies])}")
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
            if card.get('heal_power', 0) > 0 and damaged_enemies:
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

    def apply_card_effect(self, actor, card, target, is_effect = False, effect_logs = None):
        """Calculates and applies card damage or healing."""
        actor_stats = actor.get_scaled_stats()
        card_name = card['name']

        if card.get('is_wait'):
            self.combat_log.append(CombatMessage(0, f"{actor.name} waited."))

        targets = []
        if card.get('target') == 'all_enemies':
            targets = [e for e in (self.enemies if actor in self.allies else self.allies)]
        elif card.get('target') == 'all_allies':
            targets = [e for e in (self.allies if actor in self.allies else self.enemies)]
        elif card.get('target') == 'self':
            targets = [actor]
        elif target:
            targets = [target]

        print(f"[Combat!] Applying card {card_name} to {targets}")
        if effect_logs is None:
            effect_logs = []

        # Heal calculation
        if 'heal_power' in card:
            heal_stat_name = card.get('heal_stat', '')
            heal_amount = int(card['heal_power'])
            if heal_stat_name:
                heal_stat = actor_stats.get(heal_stat_name, actor_stats.get('brute_intensity', 2))
                heal_amount = int(round(heal_amount * heal_stat))
            
            for t in targets:
                if t and t.is_alive() or card.get('revive'):
                    t.current_hp = min(t.max_hp, t.current_hp + heal_amount)
                    effect_logs.append(f" on {t.name}, healing {heal_amount} HP")

        # Damage calculation
        if 'damage_power' in card:
            dmg_type = card.get('damage_type', 'melee_damage')
            base_power = card.get('damage_power')

            # Attacker stat
            atk_val = actor.get_combat_scaled_stat(dmg_type)

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
                effect_logs.append(f" on {t.name} for {dmg} damage")

                if t.current_hp == 0 and card.get('can_recruit') and getattr(self, 'is_recruitable', False):
                    t.is_recruited = True
                    effect_logs.append(f" <span style='color:var(--accent-green)'>{t.name} was successfully recruited</span>")

        # status effect caclulatoin
        if 'status_effect_target_stat' in card:
            target_stat = card['status_effect_target_stat']
            status_effect_power = card.get('status_effect_power', 1)
            status_effect_stat = card.get('status_effect_stat')
            status_effect_duration = card.get('status_effect_duration', 1)
            status_effect_duration_type = card.get('status_effect_duration_stat')
            
            status_effect_val = status_effect_power
            if status_effect_stat:
                status_effect_val = int(round(actor.get_combat_scaled_stat(status_effect_stat) * status_effect_val))

            status_effect_duration_val = status_effect_duration
            if status_effect_duration_type:
                status_effect_duration_val = int(round(actor.get_combat_scaled_stat(status_effect_duration_type) * status_effect_duration_val))
            
            for t in targets:
                if not t or not t.is_alive():
                    continue
                
                effect = StatusEffect(target_stat, status_effect_val, status_effect_duration_val)
                t.add_status_effect(effect)

                if status_effect_val > 0:
                    effect_logs.append(f" on {t.name}, {stat_name(target_stat)} has been increased by {status_effect_val}")
                else:
                    effect_logs.append(f" on {t.name}, {stat_name(target_stat)} has been decreased by {status_effect_val}")

        # ally only effects
        if actor in self.allies:

            # discard cards
            discard_cards = card.get('discard_cards', 0)
            for _ in range(discard_cards):
                if self.hand:
                    self.hand.remove(self.hand[0])
                    effect_logs.append(f" Discarded {discard_cards} cards")

            # draw reqs
            draw_req = card.get('draw_req', [])
            if draw_req:
                self.draw_reqs.append(draw_req) 

        # recur onto bonus effects
        for effect in card.get('effects', []):
            effect = dict(effect)
            if not 'name' in effect:
                effect['name'] = card_name
            if not 'target' in effect:
                effect['target'] = card.get('target')

            self.apply_card_effect(actor, effect, target, True, effect_logs)

        # Using "description as a proxy for cards vs. card effects"
        if not is_effect:
            effect_logs_text = ";".join(effect_logs)
            log_text = f"{actor.name} used {card_name}{effect_logs_text}!"
            self.combat_log.append(CombatMessage(0, log_text, card_name))
            def get_tick_info_string(character):
                status_effect_string = ', '.join([f'{s.action_timer}' for s in character.status_effects])
                return f'{character.name}: {character.action_timer} ticks ({status_effect_string})'

            print(f"[Combat!] Turn complete: {', '.join([get_tick_info_string(c) for c in self.allies + self.enemies])}")

    def execute_player_turn(self, actor, card_name, target_id):
        """Processes player character turn using card_name and target_id."""
        self.combat_log.append(CombatMessage(3, f"<span style='color:var(--accent-cyan)'>{actor.name}\'s Turn!</span>"))
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
            self.combat_log.append(CombatMessage(2, "All enemies were defeated! Take a momment to catch your breath, and venture on."))
            return True
        elif not allies_alive:
            self.is_over = True
            self.victory = False
            self.combat_log.append(CombatMessage(1, "All party members were downed, there's nothing left to do but flee."))
            return True
        return False

    def to_dict(self):
        return {
            'allies': [a.to_dict() for a in self.allies],
            'enemies': [e.to_dict() for e in self.enemies],
            'shared_deck': self.shared_deck,
            'is_recruitable': getattr(self, 'is_recruitable', False),
            'reward_card': getattr(self, 'reward_card', None),
            'reward_gold': getattr(self, 'reward_gold', 0),
            'combat_log': [msg.to_dict() for msg in self.combat_log],
            'is_over': self.is_over,
            'victory': self.victory,
            'draw_pile': self.draw_pile,
            'discard_pile': self.discard_pile,
            'hand': self.hand,
            'draw_reqs': self.draw_reqs,
        }

    @classmethod
    def from_dict(cls, d):
        allies = [Character.from_dict(a) for a in d.get('allies', [])]
        enemies = [Character.from_dict(e) for e in d.get('enemies', [])]
        engine = cls(allies, enemies, d.get('shared_deck', []), is_recruitable=d.get('is_recruitable', False), reward_card=d.get('reward_card'), reward_gold=d.get('reward_gold'))
        engine.combat_log = [CombatMessage.from_dict(msg) for msg in d.get('combat_log', [])]
        engine.is_over = d.get('is_over', False)
        engine.victory = d.get('victory', False)
        engine.draw_pile = d.get('draw_pile', [])
        engine.discard_pile = d.get('discard_pile', [])
        engine.hand = d.get('hand', [])
        engine.draw_reqs = d.get('draw_reqs', [])
        return engine


class Message:
    def __init__(self, importance, text, card_name=None):
        self.importance = importance
        self.text = text
        self.card_name = card_name

    @property
    def card(self):
        if self.card_name:
            return CARDS[self.card_name]
        else:
            return None

    @property
    def button_text(self):
        if self.card:
            return "Edit Deck"
        else:
            return ""

    @property
    def button_action(self):
        if self.card:
            return "open_deck_menu"
        else:
            return ""
    
    def to_dict(self):
        return {
            'importance': self.importance,
            'text': self.text,
            'card_name': self.card_name
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d['importance'], d['text'], d.get('card_name'))

class CombatMessage(Message):

    MIN_RARITY = 'odd'

    def __init__(self, importance, text, card_name=None):
        super().__init__(importance, text, card_name)

    @property
    def card(self):
        rarity = CARDS.get(self.card_name, {}).get('rarity', '')
        if self.card_name and ((rarity not in RARITIES) or (RARITIES.index(rarity) < RARITIES.index(self.MIN_RARITY))):
            return None
        else:
            return super().card

    @property
    def button_text(self):
        return ""

    @property
    def button_action(self):
        return ""


# --- HELPER: INITIAL GAME STATE CREATION ---

def create_initial_game_state():
    """Initializes standard starting game state per gdd.txt."""
    from .map import DEFAULT_START_INN_ID, get_inn_coords, calculate_map_pan
    from .quests import check_quest_triggers

    start_x, start_y = get_inn_coords(DEFAULT_START_INN_ID)
    pan_x, pan_y = calculate_map_pan(start_x, start_y)

    # Starting character: 1 Level 1 Fox Wandering Spellsword
    hero = Character(name="Yew", species="Fox", current_class="Wandering Spellsword")
    
    party = Party()
    party.x = start_x
    party.y = start_y
    party.members.append(hero)
    
    # Starting cards per GDD: 5 health potions, 6 slashes, 3 light clothes
    starting_inventory = (
        ['Potion'] * 4 +
        ['Woe'] * 1
    )
    party.inventory = starting_inventory
    party.shared_deck = ( 
        ['Bargain'] +
        ['Slash'] * 4 +
        ['Potion'] * 2 +
        ['Woe'] * 3
    )

    state = {
        'screen': 'overworld',  # Will be set to 'dialog' by initial quest trigger
        'quests': {
            'voinara_intro': 0,
            'badgys_errand': 0,
        },
        'pan_x': pan_x,
        'pan_y': pan_y,
        'party': party.to_dict(),
        'inns': {},
        'current_inn_id': DEFAULT_START_INN_ID,
        'respawn_inn_id': DEFAULT_START_INN_ID,
        'library_cards': [],
        'active_menu': None,  # None, 'character_menu', 'shop', 'inn', 'combat'
        'combat': None,
        'log': [Message(1, "...").to_dict()],
    }

    # Trigger initial quest check so voinara_intro step 0 procs immediately
    check_quest_triggers(state, party)

    return state


from django import template

register = template.Library()

@register.filter
def percent_pips(value, num_pips):
    return [ (i/num_pips) < value for i in range(num_pips) ]


@register.filter
def count_pips(num_pips):
    return range(max(num_pips, 0))

MAP_CHARACTERS_TO_SYMBOLS = {
    'f': "↟",
    'S': "⌂",
    'B': "⌂",
    'I': "☗",
    ' ': "&nbsp;",
}

@register.filter
def map_space(char):
    return MAP_CHARACTERS_TO_SYMBOLS.get(char, char)

DEFAULT_ILLUST = """
+-----------------+
|                 |
|                 |
|                 |
|                 |
|                 |
+-----------------+
"""

@register.filter
def illust(illust):
    if not illust:
        illust = DEFAULT_ILLUST
    if illust[0] == "\n":
        illust = illust[1:]
    if illust[-1] == "\n":
        illust = illust[:-1]
    return illust

@register.filter
def damage_type(value):
    return value.replace("_damage", "").replace("_intensity", "").upper()

@register.filter
def stat_name(name):
    format_name = name.replace("_", " ").title()
    format_name = format_name.replace("Moon", "Moon Magic").replace("Star", "Star Magic").replace("Void", "Void Magic")
    return format_name

STAT_NAME_REPLACEMENTS = {
        "melee": "M",
        "ranged": "R",
        "survival": "S",
        "moon": "☾",
        "star": "☀︎",
        "void": "∅",
        "brute": "B",
        "_intensity": "",
        "_damage": "D",
        "_resistance": "R",
        "_vulnerability": "V",
        "nimbleness": "N",
    }

@register.filter
def short_stat_name(name):
    for replacement in STAT_NAME_REPLACEMENTS:
        name = name.replace(replacement, STAT_NAME_REPLACEMENTS[replacement])
    return name

@register.filter
def all_effects(card):
    return [card] + card.get('effects', [])

DISPLAYED_EFFECTS_KEYS = [
    'damage_power',
    'damage_type',
    'heal_power',
    'heal_stat',
    'status_effect_power',
    'status_effect_stat',
    'status_effect_duration',
    'status_effect_duration_stat',
]

@register.filter
def all_unique_effects(card):
    effects = []
    for effect in all_effects(card):
        unique = True
        for existing_effect in effects:
            for key in DISPLAYED_EFFECTS_KEYS:
                if effect.get(key) != existing_effect.get(key):
                    break
            else:
                unique = False
                break
        if unique:
            effects.append(effect)
    return effects

@register.filter
def can_equip(character, card):
    return character.can_equip_card(card)[0]

@register.filter
def signed(val):
    if val > 0:
        return f"+{val}"
    else:
        return f"{val}"

@register.filter
def negate(val):
    return not val
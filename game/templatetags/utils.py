from django import template

register = template.Library()

@register.filter
def percent_pips(value, num_pips):
    return [ (i/num_pips) < value for i in range(num_pips) ]

@register.filter
def damage_type(value):
    return value.replace("_damage", "").replace("_intensity", "").upper()

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
def stat_name(name):
    format_name = name.replace("_", " ").title()
    format_name = format_name.replace("Moon", "Moon Magic").replace("Star", "Star Magic").replace("Void", "Void Magic")
    return format_name

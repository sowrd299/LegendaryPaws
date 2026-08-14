from django import template

register = template.Library()

@register.filter
def percent_pips(value, num_pips):
    return [ (i/num_pips) < value for i in range(num_pips) ]

@register.filter
def damage_type(value):
    return value.replace("_damage", "").replace("_intensity", "").upper()
from django import template

register = template.Library()

@register.filter
def percentpips(value, num_pips):
    return [ (i/num_pips) < value for i in range(num_pips) ]

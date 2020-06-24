from django import template

register = template.Library()

@register.filter()
def price_format(value):
    """Return format price"""
    return '${0:2}'.format(value)

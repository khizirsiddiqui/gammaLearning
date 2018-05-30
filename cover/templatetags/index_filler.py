from django import template
from scripts.quotes import read_quotes

register = template.Library()


@register.simple_tag
def get_random_quote():
    quote = read_quotes()
    return {'quote': quote}

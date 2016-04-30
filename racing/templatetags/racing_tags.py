import random

from django import template


register = template.Library()


@register.simple_tag
def random_header():
    # These map to CSS classes, for the header background images.
    options = [
        'srvcross-1',
        'srvcross-2',
        'srvrally-1',
        'srvrally-2',
        'stadium-1',
        'stadium-2',
        'surface-1',
        'surface-2',
        'surface-3',
        'zerogravity-1',
        'zerogravity-2',
    ]

    return random.choice(options)

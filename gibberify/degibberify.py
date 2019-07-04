"""
Create reverse translation dictionaries
"""


# local imports
from .utils import access_data


def unscramble(lang_in, lang_out):
    """
    reads an existing translation dictionary

    returns a reversed dictionary
    """
    straight = access_data('dicts', lang_in, lang_out)

    reversed = {}
    for ln, mappings in straight.items():
        reversed[ln] = {k: v for v, k in mappings.items()}

    print(straight['1'],'\n', reversed['1'])
    return reversed


unscramble('en', 'orc')

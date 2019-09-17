# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Generate reverse dictionaries to (partially) understand gibberish
"""

# local imports
from .. import utils


def unscramble(straight):
    """
    reads an existing translation dictionary and reverses it

    returns the reversed dictionary
    """
    reverse = {}

    all_reverse = {k: v for mappings in straight.values() for v, k in mappings.items()}

    # sort by length
    for k, v in all_reverse.items():
        ln = len(k)
        if ln not in reverse.keys():
            reverse[ln] = {}
        reverse[ln][k] = v

    return reverse


def build_reverse_dicts(gib_langs, real_langs):
    """
    creates and saves a reverse dict for every language combination
    """
    # this has no "if exists" check, because it's fast it doesn't matter
    for gib_lang in gib_langs:
        for real_lang in real_langs:
            straight = utils.access_data('dicts', real_lang, gib_lang)
            reverse = unscramble(straight)
            utils.access_data('dicts', gib_lang, real_lang, reverse)

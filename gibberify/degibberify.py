# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Reverse translate from gibberish to real languages
"""

import os
import re

# local imports
from .config import __real_langs__, __gib_langs__
from .utils import access_data, __data__


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


def build_reverse_dicts():
    """
    creates and saves a reverse dict for every language combination
    """
    # check whether straight dictionaries exist
    for lang in __real_langs__:
        for gib_lang in __gib_langs__.keys():
            dict_file = os.path.join(__data__, 'dicts', f'{lang}-{gib_lang}.json')
        if not os.path.isfile(dict_file):
            raise FileNotFoundError(f'dictionary file for {lang}-{gib_lang} does not exist. '
                                    f'You need to generate it first!')

    # make them all!
    for gib_lang_in in __gib_langs__.keys():
        for lang_out in __real_langs__:
            straight = access_data('dicts', lang_out, gib_lang_in)
            reverse = unscramble(straight)
            access_data('dicts', gib_lang_in, lang_out, reverse)


def degibberify(translator, text):
    """
    translate a text from real language into a specified gibberish language

    returns something that may resemble the original message
    """
    # get list of lengths
    lns = list(translator.keys())
    lns.sort(reverse=True)

    trans = text.lower()
    trans_tmp = trans
    for ln in lns:
        for syl, mapping in translator[ln].items():
            for match in re.finditer(syl, trans_tmp):
                start, end = match.span()
                trans_tmp = ''.join([c for c in trans_tmp[:start]] +
                                    ['�'] * len(mapping) +
                                    [x for x in trans_tmp[end:]])
                trans = ''.join([c for c in trans[:start]] +
                                [c for c in mapping] +
                                [x for x in trans[end:]])
    return trans

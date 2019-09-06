# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Reverse translate from gibberish to real languages
"""

import os
import re

# local imports
from . import config
from . import utils
from .scramble import build_dicts


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


def build_all_dicts(force_rebuild=False):
    """
    creates and saves a reverse dict for every language combination
    """
    conf = config.import_conf()

    # force rebuild of straight dictionaries if asked
    if force_rebuild:
        build_dicts()
    else:
        # check whether straight dictionaries exist, run scramble if needed
        for real_lang in conf['real_langs']:
            for gib_lang in conf['gib_langs']:
                dict_file = utils.clean_path(utils.data, 'dicts', f'{real_lang}-{gib_lang}.json')
            if not os.path.isfile(dict_file):
                build_dicts()

    # make them all!
    for gib_lang in conf['gib_langs']:
        for real_lang in conf['real_langs']:
            straight = utils.access_data('dicts', real_lang, gib_lang)
            reverse = unscramble(straight)
            utils.access_data('dicts', gib_lang, real_lang, reverse)


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

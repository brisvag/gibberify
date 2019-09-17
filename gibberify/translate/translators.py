# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Translate real languages in gibberish (and vice-versa) based on pre-generated translation dictionaries
"""

import re
import sys
import random

# local imports
from .. import utils
from .. import config


def gibberify(translator, text):
    """
    translate a text from real language into a specified gibberish language

    returns translated string
    """

    # split words maintaining non-word characters in the right positions
    words = re.split(r'(\W+)(\w+)', text)

    # generate translation based on syllables
    trans_list = []
    # use syllabize to break down into syllables
    for w in words:
        # leave non-word parts of the sentence as is
        if re.match(r'\w+', w):
            syl = utils.syllabize(w)
            # check for translation in corresponding length
            # translate syllables only if they are found, otherwise return a random one
            trans_syl = [translator[str(len(s))].get(s.lower(),
                                                     random.choice(list(translator[str(len(s))].keys())))
                         if str(len(s)) in translator.keys()
                         # also return a random one if syllable length is too high, instead of crashing
                         else random.choice(list(random.choice(list(translator.values())).values()))
                         for s in syl]
            # save word translation
            trans_w = ''.join(trans_syl)
            # let's preserve capitalisation, at least a bit
            if w[0].isupper():
                if w.isupper() and len(w) >= 2:
                    trans_w = trans_w.upper()
                else:
                    trans_w = trans_w.capitalize()
        else:
            trans_w = w

        trans_list.append(trans_w)

    # join everything
    trans = ''.join(trans_list)

    # remove multiple spaces due to input or unmapped syllables
    trans = re.sub(' +', ' ', trans)

    return trans


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


def direct_translator(lang_in, lang_out, text):
    """
    translates using gibberify or degibberify directly, without the need of passing a "translator" dictionary

    useful for command line translation and module import
    """
    conf = config.import_conf()

    if lang_in in conf['real_langs'] and lang_out in conf['gib_langs'].keys():
        translate = gibberify
    elif lang_in in conf['gib_langs'].keys() and lang_out in conf['real_langs']:
        translate = degibberify
    else:
        print(f'ERROR: no dictionary from "{lang_in}" to "{lang_out}" found.\n'
              f'Are you sure it\'s not a typo?\n'
              f'Otherwise, did you generate the dictionaries first? Try with `gibberify --build-dicts`')
        sys.exit()
    translator = utils.access_data('dicts', lang_in, lang_out)

    return translate(translator, text)

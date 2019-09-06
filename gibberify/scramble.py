# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Generate fake, gibberish translation dictionaries to be used by the translator
"""

import random
import os

# local imports
from . import utils
from . import config
from .syllabize import build_syllables


def scramble(lang_in, langs_out):
    """
    semi-randomly links syllables from the input pool (one language) to ones
    in the target pools (multiple languages) in order to form translation dictionaries

    returns a dict that can be used to translate (almost) every syllable from the input language
    """
    trans_dict = {}

    # load the required languages
    pool_in = utils.access_data('syllables', lang_in)
    pool_out = {}
    for lang_out in langs_out:
        pool_out_part = utils.access_data('syllables', lang_out)
        for ln, syls in pool_out_part.items():
            if ln not in pool_out.keys():
                pool_out[ln] = []
            pool_out[ln].extend(syls)
    # remove duplicates syllables from different languages
    for ln, syls in pool_out.items():
        pool_out[ln] = list(set(syls))

    pool_in_total = [syl for syls in pool_in.values() for syl in syls]
    pool_out_total = [syl for syls in pool_out.values() for syl in syls]

    # scramble!
    random.shuffle(pool_out_total)

    # make sure we do enough times to map to all the input syllables (should not be a problem, but you never know)
    ratio = len(pool_in_total) // len(pool_out_total)
    tmp_pool = pool_out_total
    for _ in range(ratio):
        random.shuffle(tmp_pool)
        pool_out_total.extend(tmp_pool)

    for ln_in, syls_in in pool_in.items():
        # maintain length discrimination for later utility
        trans_dict[ln_in] = {}
        # create subpool of syllables (more list comprehension black magic!)
        # do the actual mapping
        for syl_in in syls_in:
            mapping = pool_out_total.pop()
            trans_dict[ln_in][syl_in] = mapping

    return trans_dict


def make_dict(lang_in, gib_lang_out):
    """
    takes a real language string and a fake language dictionary (with relative settings) as input and
    uses scramble to generate a translation dictionary and saves it to file

    returns nothing
    """
    # unpack translation settings
    langs_out = config.gib_langs[gib_lang_out]['pool']

    # create actual translation dictionary
    print(f'Creating translation dictionary "{lang_in}-{gib_lang_out}"')
    trans_dict = scramble(lang_in, langs_out)

    utils.access_data('dicts', lang_in, gib_lang_out, write_data=trans_dict)


def build_dicts():
    """
    builds a translation dictionary for all the required language combinations
    """
    # import config
    conf = config.import_conf()

    # make sure directories exist
    dict_dir = utils.clean_path(utils.data, 'dicts')
    if not os.path.exists(dict_dir):
        os.makedirs(dict_dir)

    # check whether syllable pools exist, and make them if needed
    for lang in conf['real_langs']:
        syl_file = utils.clean_path(utils.data, 'syllables', f'{lang}.json')
        if not os.path.isfile(syl_file):
            build_syllables(download=False)

    # make dictionary generation somewhat deterministic, cause why not TODO: this clearly does nothing
    random.seed('gibberify')

    # make them all!
    for real_lang in conf['real_langs']:
        for gib_lang, gib_lang_conf in conf['gib_langs'].items():
            make_dict(real_lang, gib_lang, gib_lang_conf)


if __name__ == '__main__':
    build_dicts()

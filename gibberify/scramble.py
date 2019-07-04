"""
Generate fake, gibberish translation dictionaries to be used by the translator
"""

import random
import os

# local imports
from .config import __real_langs__, __gib_langs__
from .utils import access_data, __data__


def scramble(lang_in, langs_out):
    """
    semi-randomly links syllables from the input pool (one language) to ones
    in the target pools (multiple languages) in order to form translation dictionaries

    returns a dict that can be used to translate (almost) every syllable from the input language
    """
    trans_dict = {}

    # load the required languages
    pool_in = access_data('syllables', lang_in)
    pool_out = {}
    for lang_out in langs_out:
        pool_out_part = access_data('syllables', lang_out)
        for ln, syls in pool_out_part.items():
            if ln not in pool_out.keys():
                pool_out[ln] = []
            pool_out[ln].extend(syls)
    # remove duplicates syllables from different languages
    for ln, syls in pool_out.items():
        pool_out[ln] = list(set(syls))

    # TODO: would be nice not to have duplicate mappings, but my attempts using a while loop were
    #       unsuccessful/ridiculously expensive
    #       for now, generate new syllables until we have mapped every syllable to something

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
        # maintain length discrimination for better translation TODO: is this really useful?
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
    langs_out = __gib_langs__[gib_lang_out]['pool']

    # create actual translation dictionary
    print(f'Creating translation dictionary "{lang_in}-{gib_lang_out}"')
    trans_dict = scramble(lang_in, langs_out)

    access_data('dicts', lang_in, gib_lang_out, write_data=trans_dict)


def build_dicts():
    """
    builds a translation dictionary for all the required language combinations
    """
    # make sure directories exist
    dict_dir = os.path.join(__data__, 'dicts')
    if not os.path.exists(dict_dir):
        os.makedirs(dict_dir)

    # check whether syllable pools exist
    for lang in __real_langs__:
        syl_file = os.path.join(__data__, 'syllables', f'{lang}.json')
        if not os.path.isfile(syl_file):
            raise FileNotFoundError(f'syllable file for {lang} does not exist. You need to generate it first!')

    # make dictionary generation somewhat deterministic, cause why not TODO: this clearly does nothing
    random.seed('gibberify')

    # make them all!
    for lang_in in __real_langs__:
        for gib_lang_out in __gib_langs__.keys():
            make_dict(lang_in, gib_lang_out)


if __name__ == '__main__':
    build_dicts()

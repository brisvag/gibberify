"""
Generate fake, gibberish translation dictionaries to be used by the translator
"""

import json
import random
import sys
import os

# local imports
from .config import __real_langs__, __gib_langs__
from .utils import code, __data__


def scramble(lang_in, langs_out):
    """
    semi-randomly links syllables from the input pool (one language) to ones
    in the target pools (multiple languages) in order to form translation dictionaries

    returns a dict that can be used to translate (almost) every syllable from the input language
    """
    trans_dict = {}

    # load the required languages
    with open(os.path.join(__data__, 'syllables', f'{lang_in}.json')) as f:
        pool_in = {int(length): set(syllables) for length, syllables in json.load(f).items()}
    pool_out = {}
    for lang_out in langs_out:
        with open(os.path.join(__data__, 'syllables', f'{lang_out}.json')) as f:
            for ln, syls in json.load(f).items():
                if ln not in pool_out.keys():
                    pool_out[int(ln)] = set()
                pool_out[int(ln)].update(syls)

    # TODO: would be nice not to have duplicate mappings, but my attempts using a while loop were
    #       unsuccessful/ridiculously expensive
    # generate new syllables until we have mapped every syllable to something

    for ln_in, syls_in in pool_in.items():
        # create subpool of syllables (more black magic!)
        subpool = [syl_out for ln_out, syls_out in pool_out.items() for syl_out in syls_out]
        # TODO use syllable length for something meaningful
        for syl_in in syls_in:
            # get a random number between 0 and 2, so syllable mapping is not 1 to 1.
            # weights are arbitrary: 10% `0`, 80% `1`, 10% `2`. This way we shouldn't end up with
            # too many empty words or very long ones
            weights = [0] + [1] * 8 + [2]
            r = random.choice(weights)
            mapping = ''.join(random.sample(subpool, r))
            trans_dict[syl_in] = mapping

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

    with open(os.path.join(__data__, 'dicts', f'{lang_in}-{gib_lang_out}.json'), 'w+') as outfile:
        json.dump(trans_dict, outfile, indent=2)


def build():
    """
    builds a translation dictionary for all the required language combinations
    """
    # make sure directories exist
    os.path.join(__data__, 'dicts')

    # make dictionary generation somewhat deterministic, cause why not TODO: this clearly does nothing
    random.seed('gibberify')

    # make them all!
    for lang_in in __real_langs__:
        for lang_out in __gib_langs__.keys():
            make_dict(code(lang_in), lang_out)


if __name__ == '__main__':
    build()

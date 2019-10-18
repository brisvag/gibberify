# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

import random

# local imports
from .. import utils


class Scrambler:
    """
    Scrambler class

    based on a given configuration, generates a straight and reverse
    dictionary for the given combination of languages
    """
    def __init__(self, real_lang, gib_lang, gib_conf):
        self.real_lang = real_lang
        self.gib_lang = gib_lang
        self.gib_conf = gib_conf
        self.real_pool = None
        self.gib_pool_raw = None
        self.gib_pool = None
        self.dict_straight = None
        self.dict_reverse = None

    def load_real_pool(self):
        """
        loads all the syllables from the required real language
        """
        self.real_pool = utils.access_data('syllables', self.real_lang)

    def load_gib_pool_raw(self):
        """
        loads all the syllables needed for the gibberish language from a list of real languages
        """
        pool = set()
        for lang in self.gib_conf["pool"]:
            pool_part = utils.access_data('syllables', lang)
            pool.update(pool_part)

        self.gib_pool_raw = list(pool)

    def create_gib_pool(self):
        """
        creates a customized pool of syllables to be used by the gibberish language by
        applying several options defined in the provided configuration
        """
        pool_out = self.gib_pool_raw

        # get rid of part of the syllables NOT containing enriched patterns
        for pattern in self.gib_conf["enrich"]:
            # get rid of 50% of syllables containing pattern
            temp_pool = [syl for syl in pool_out if pattern in syl or random.choices([True, False], [0.5, 0.5])[0]]
            pool_out = temp_pool

        # get rid of part of the syllables containing impoverished patterns
        for pattern in self.gib_conf["impoverish"]:
            # get rid of 50% of syllables containing pattern
            temp_pool = [syl for syl in pool_out if pattern not in syl or random.choices([True, False], [0.5, 0.5])[0]]
            pool_out = temp_pool

        # get rid of ALL the syllables containing forbidden patterns
        for pattern in self.gib_conf["remove"]:
            # get rid of all the syllables containing pattern
            temp_pool = [syl for syl in pool_out if pattern not in syl]
            pool_out = temp_pool

        self.gib_pool = list(pool_out)

    def straight(self):
        """
        semi-randomly links syllables from the input pool (one language) to ones
        in the target pools (multiple languages) in order to form a translation dictionary

        generates a dict that can be used to translate (almost) every syllable from the input language
        """
        print(f'Creating translation dictionary from {utils.r_lang_codes[self.real_lang]} to {self.gib_lang}...')
        trans_dict = {}

        # TODO: use shorter syllables more often, like in normal languages
        # make sure we do enough times to map to all the input syllables (should not be a problem, but you never know)
        ratio = len(self.real_pool) // len(self.gib_pool)
        tmp_gib_pool = self.gib_pool
        final_gib_pool = tmp_gib_pool
        for _ in range(ratio):
            random.shuffle(tmp_gib_pool)
            final_gib_pool.extend(tmp_gib_pool)

        # do the actual mapping
        # TODO: add some customization to mapping (length?...)
        for syl_real in self.real_pool:
            syl_gib = final_gib_pool.pop()
            trans_dict[syl_real] = syl_gib

        self.dict_straight = trans_dict

    def reverse(self):
        """
        takes an existing translation dictionary from real to gibberish and reverses it
        """
        print(f'Creating translation dictionary from {self.gib_lang} to {utils.r_lang_codes[self.real_lang]}...')
        reverse = {}

        all_reverse = {k: v for v, k in self.dict_straight.items()}

        # sort by length, needed for reverse translation
        # TODO: not sure this is really true. Need more testing.
        for k, v in all_reverse.items():
            ln = len(k)
            if ln not in reverse.keys():
                reverse[ln] = {}
            reverse[ln][k] = v

        self.dict_reverse = reverse

    def write(self):
        """
        writes to file the generated data
        """
        utils.access_data('dicts', self.real_lang, self.gib_lang, write_data=self.dict_straight)
        utils.access_data('dicts', self.gib_lang, self.real_lang, write_data=self.dict_reverse)

    def run(self):
        """
        main class method, runs all the other methods and writes to file
        """
        self.load_real_pool()
        self.load_gib_pool_raw()
        self.create_gib_pool()
        self.straight()
        self.reverse()
        self.write()

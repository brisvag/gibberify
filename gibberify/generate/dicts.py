# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

import random

# local imports
from .. import utils


class GibDict(dict):
    """
    dict class to represent a gibberify translation dictionary
    """
    def __init__(self, lang_in, lang_out, gib_conf, *args, reverse=False, **kwargs):
        super(GibDict, self).__init__(*args, **kwargs)
        self.lang_in = lang_in
        self.lang_out = lang_out
        self.conf = gib_conf
        self.version = utils.__version__
        self.reverse = reverse


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

    def _exists(self):
        """
        make sure that a dictionary with same configuration does not already exist
        :return: True if the same dictionary already exists, False otherwise
        """
        try:
            old = utils.access_data('dicts', self.real_lang, self.gib_lang)
        except FileNotFoundError:
            return False
        if old.conf != self.gib_conf:
            return False
        return True

    def _load_real_pool(self):
        """
        loads all the syllables from the required real language
        """
        return utils.access_data('syllables', self.real_lang)

    def _load_gib_pool_raw(self):
        """
        loads all the syllables needed for the gibberish language from a list of real languages
        """
        pool = set()
        for lang in self.gib_conf['pool']:
            pool_part = utils.access_data('syllables', lang)
            pool.update(pool_part)

        return list(pool)

    def _create_gib_pool(self):
        """
        creates a customized pool of syllables to be used by the gibberish language by
        applying several options defined in the provided configuration
        """
        pool_out = self.gib_pool_raw

        # get rid of part of the syllables NOT containing enriched patterns
        for pattern in self.gib_conf['enrich']:
            # get rid of 50% of syllables containing pattern
            temp_pool = [syl for syl in pool_out if pattern in syl or random.choices([True, False], [0.5, 0.5])[0]]
            pool_out = temp_pool

        # get rid of part of the syllables containing impoverished patterns
        for pattern in self.gib_conf['impoverish']:
            # get rid of 50% of syllables containing pattern
            temp_pool = [syl for syl in pool_out if pattern not in syl or random.choices([True, False], [0.5, 0.5])[0]]
            pool_out = temp_pool

        # get rid of ALL the syllables containing forbidden patterns
        for pattern in self.gib_conf['remove']:
            # get rid of all the syllables containing pattern
            temp_pool = [syl for syl in pool_out if pattern not in syl]
            pool_out = temp_pool

        return list(pool_out)

    def _make_straight(self):
        """
        semi-randomly links syllables from the input pool (one language) to ones
        in the target pools (multiple languages) in order to form a translation dictionary

        generates a dict that can be used to translate (almost) every syllable from the input language
        """
        print(f'Creating translation dictionary from {utils.r_lang_codes[self.real_lang]} to {self.gib_lang}...')
        trans_dict = GibDict(self.real_lang, self.gib_lang, self.gib_conf)

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

        return trans_dict

    def _make_reverse(self):
        """
        takes an existing translation dictionary from real to gibberish and reverses it
        """
        print(f'Creating translation dictionary from {self.gib_lang} to {utils.r_lang_codes[self.real_lang]}...')
        rev = GibDict(self.gib_lang, self.real_lang, self.gib_conf, reverse=True)

        all_reverse = {k: v for v, k in self.dict_straight.items()}

        # sort by length, needed for reverse translation
        # TODO: not sure this is really true. Need more testing.
        for k, v in all_reverse.items():
            ln = len(k)
            if ln not in rev.keys():
                rev[ln] = {}
            rev[ln][k] = v

        return rev

    def _save(self):
        """
        writes to file the generated data
        """
        utils.access_data('dicts', self.real_lang, self.gib_lang, write_data=self.dict_straight)
        utils.access_data('dicts', self.gib_lang, self.real_lang, write_data=self.dict_reverse)

    def run(self, force=False):
        """
        main class method, runs all the other methods and saves dicts to file
        """
        if self._exists() and not force:
            return
        self.real_pool = self._load_real_pool()
        self.gib_pool_raw = self._load_gib_pool_raw()
        self.gib_pool = self._create_gib_pool()
        self.dict_straight = self._make_straight()
        self.dict_reverse = self._make_reverse()
        self._save()

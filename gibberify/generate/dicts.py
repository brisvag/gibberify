import random

# local imports
from .. import utils


class Scrambler():
    """
    Scrambler class. Based on a given configuration, generates a straight and reverse dictionary
    for the given combination of languages
    of all the data needed to make custom dictionaries
    """

    def __init__(self, real_lang, gib_lang, gib_conf):
        self.real_lang = real_lang
        self.gib_lang = gib_lang
        self.gib_conf = gib_conf
        self.real_pool = None
        self.gib_pool = None
        self.dict_straight = None
        self.dict_reverse = None

    def create_gib_pool(self):
        """
        creates a customized pool of syllables to be used by the gibberish language by merging
        multiple languages and applying several options defined in the provided configuration
        """
        # first create the base pool
        pool_out = set()
        for lang in self.gib_conf["pool"]:
            pool_out_part = utils.access_data('syllables', lang)
            pool_out.update(pool_out_part)

        # get rid of part of the syllables NOT containing enriched patterns
        for pattern in self.gib_conf["enrich"]:
            # get rid of 30% of syllables containing pattern
            temp_pool = [syl for syl in pool_out if pattern in syl or random.choices([True, False], [0.7, 0.3])[0]]
            pool_out = temp_pool

        # get rid of part of the syllables containing impoverished patterns
        for pattern in self.gib_conf["impoverish"]:
            # get rid of 30% of syllables containing pattern
            temp_pool = [syl for syl in pool_out if pattern not in syl or random.choices([True, False], [0.7, 0.3])[0]]
            pool_out = temp_pool

        # get rid of ALL the syllables containing forbidden patterns
        for pattern in self.gib_conf["remove"]:
            # get rid of all the syllables containing pattern
            temp_pool = [syl for syl in pool_out if pattern not in syl]
            pool_out = temp_pool

        self.gib_pool = pool_out

    def straight(self):
        """
        semi-randomly links syllables from the input pool (one language) to ones
        in the target pools (multiple languages) in order to form a translation dictionary

        generates a dict that can be used to translate (almost) every syllable from the input language
        """
        print(f'Creating translation dictionary for "{self.real_lang}-{self.gib_lang}"')
        trans_dict = {}

        # load the required languages
        self.real_pool = utils.access_data('syllables', self.real_lang)

        # make sure we do enough times to map to all the input syllables (should not be a problem, but you never know)
        ratio = len(self.real_pool) // len(self.gib_pool)
        tmp_gib_pool = self.gib_pool
        final_gib_pool = tmp_gib_pool
        for _ in range(ratio):
            random.shuffle(tmp_gib_pool)
            final_gib_pool.extend(tmp_gib_pool)

        # do the actual mapping
        for syl_real in self.real_pool:
            syl_gib = final_gib_pool.pop()
            trans_dict[syl_real] = syl_gib

        self.dict_straight = trans_dict

    def reverse(self):
        """
        takes an existing translation dictionary from real to gibberish and reverses it
        """
        print(f'Creating translation dictionary for "{self.gib_lang}-{self.real_lang}"')
        reverse = {}

        all_reverse = {k: v for v, k in self.dict_straight.items()}

        # sort by length, needed for reverse translation
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

# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

import re
import random
from pathlib import Path

# local imports
from .utils import syllabize, data, access_data


class Translator():
    """
    executes translations according to current configuration and inputs
    """

    def __init__(self):
        self.text_in = None
        self.text_out = None
        self.lang_in = None
        self.lang_out = None
        self.dicts = self.load_dicts()
        self.dict = None

    def __setattr__(self, key, value):
        # detect if important attributes change and run appropriate methods if so
        if not hasattr(self, key) or getattr(self, key) != value:
            if key in ('lang_in', 'lang_out', 'text_in'):
                changed = True

        super(Translator, self).__setattr__(key, value)

        if changed:
            self.run()

    def load_dicts(self):
        """
        loads all generated dictionaries into memory
        """
        dicts = {}
        dicts_dir = data/'dicts'
        for dict_file in dicts_dir.iterdir():
            dict_code = dict_file.stem
            lang_in, lang_out = dict_code.split('-')
            content = access_data('dicts', lang_in, lang_out)
            dicts[dict_code] = content

        return dicts

    def gibberify(self):
        """
        translate a text from real language into a specified gibberish language

        returns translated string
        """

        # split words maintaining non-word characters in the right positions
        words = re.split(r'(\W+)(\w+)', self.text_in)

        # generate translation based on syllables
        trans_list = []
        # use syllabize to break down into syllables
        for w in words:
            # leave non-word parts of the sentence as is
            if re.match(r'\w+', w):
                syl = syllabize(w)
                # translate syllables only if they are found, otherwise return a random one
                trans_syl = [self.dict.get(s.lower(), random.choice(list(self.dict)))
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

        self.text_out = trans

    def degibberify(self):
        """
        translate a text from real language into a specified gibberish language, assuming
        that longer matching syllables are more likely to be single syllables than a combination
        of multiple small ones. WARNING: VERY HACKY!

        returns something that may resemble the original message
        """
        # get list of syllable lengths
        lns = list(self.dict.keys())
        lns.sort(reverse=True)

        trans = self.text_in
        trans_tmp = trans
        for ln in lns:
            for syl, mapping in self.dict[ln].items():
                for match in re.finditer(syl, trans_tmp):
                    start, end = match.span()
                    trans_tmp = ''.join([c for c in trans_tmp[:start]] +
                                        ['�'] * len(mapping) +
                                        [x for x in trans_tmp[end:]])
                    trans = ''.join([c for c in trans[:start]] +
                                    [c for c in mapping] +
                                    [x for x in trans[end:]])

        self.text_out = trans

    def run(self):
        """
        translates from text_in to text_out based on the current settings
        """
        # if languages are not set, set them randomly
        if not self.lang_in or not self.lang_out:
            self.lang_in = rando

        # update current dictionary
        dict_code = f'{self.lang_in}-{self.lang_out}'
        self.dict = self.dicts[dict_code]

        # check if current translator is straight or reverse
        if len(self.lang_in) == 2:
            self.gibberify()
        else:
            self.degibberify()
        # TODO: change this to something better than code length. Maybe good excuse to switch
        #       to using `pickle` and save some metadata in the files


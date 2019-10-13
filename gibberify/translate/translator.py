# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

import re
import random

# local imports
from .. import utils


class Translator:
    """
    executes translations according to current configuration and inputs
    """
    def __init__(self, lang_in=None, lang_out=None, text_in=''):
        """
        :param lang_in: language to translate from
        :param lang_out: language to transate to
        :param text_in: texto to translate
        """
        self.lang_in = lang_in
        self.lang_out = lang_out
        self.text_in = text_in
        self.text_out = ''
        self.dicts = self.load_dicts()
        self.dict = None

    def __str__(self):
        # make sure translation is performed at least once before returning
        self.run()
        return self.text_out

    def __setattr__(self, key, value):
        # detect if important attributes change and automagically run translation if so
        attr_list = ('lang_in', 'lang_out', 'text_in', 'dicts')
        changed = False
        if not hasattr(self, key) or getattr(self, key) != value:
            if key in attr_list:
                changed = True

        super(Translator, self).__setattr__(key, value)

        # only run if all attributes have a value
        if changed and all([attr in self.__dict__ for attr in attr_list]):
            self.run()

    def load_dicts(self):
        """
        loads all generated dictionaries into memory

        :return: a dict containing all the available dictionaries, with `langin-langout` as keys
        """
        dicts = {}
        dicts_dir = utils.data/'dicts'
        for dict_file in dicts_dir.iterdir():
            dict_code = dict_file.stem
            lang_in, lang_out = dict_code.split('-')
            content = utils.access_data('dicts', lang_in, lang_out)
            dicts[dict_code] = content

        return dicts

    def gibberify(self):
        """
        translate a text from real language into a specified gibberish language

        sets translation to text_out
        """

        # split words maintaining non-word characters in the right positions
        words = re.split(r'(\W+)(\w+)', self.text_in)

        # generate translation based on syllables
        trans_list = []
        # use syllabize to break down into syllables
        for w in words:
            # leave non-word parts of the sentence as is
            if re.match(r'\w+', w):
                syl = utils.syllabize(w)
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

        sets something that may resemble the original message to text_out
        """
        # get list of syllable lengths
        lns = list(self.dict.keys())
        lns.sort(reverse=True)

        # save two versions of the text which need to be processed in parallel
        trans = self.text_in
        trans_tmp = trans
        # start from longest syllables
        for ln in lns:
            for syl, mapping in self.dict[ln].items():
                # if syllable is found in the text
                for match in re.finditer(syl, trans_tmp):
                    # save start and end index of the matched syllable
                    start, end = match.span()
                    # The following shenanigans are needed because we need to make sure already replaced
                    # syllables are not matched again to a new mapping (hence the placeholders)
                    # this needs to be done with len(mapping) because matched syllables and their mappings are NOT
                    # the same length!
                    # replace matched syllable with placeholders in temp translation,
                    trans_tmp = ''.join([c for c in trans_tmp[:start]] +
                                        ['�'] * len(mapping) +
                                        [x for x in trans_tmp[end:]])
                    # replace in real translation with ACTUAL mapping
                    trans = ''.join([c for c in trans[:start]] +
                                    [c for c in mapping] +
                                    [x for x in trans[end:]])

        self.text_out = trans

    def run(self):
        """
        translates from text_in to text_out based on the current settings
        """
        # if languages are not set, do nothing
        if not self.lang_in or not self.lang_out:
            return

        # update current dictionary
        dict_code = f'{self.lang_in}-{self.lang_out}'
        try:
            self.dict = self.dicts[dict_code]
        except KeyError:
            # this is raised if the dictionary does not exist (usually because in between changes)
            return

        # check if current translator is straight or reverse
        if len(self.lang_in) == 2 and len(self.lang_out) == 3:
            self.gibberify()
        elif len(self.lang_in) == 3 and len(self.lang_out) == 2:
            self.degibberify()
        else:
            raise NotImplementedError(f'How did this happen? {self.lang_in, self.lang_out}')
        # TODO: change this to something better than code length. Maybe good excuse to switch
        #       to using `pickle` and save some metadata in the files

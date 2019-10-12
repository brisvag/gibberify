# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.


from urllib.request import urlopen
from transliterate import translit, get_available_language_codes
import json
import certifi
from time import sleep
import os

# local imports
from .. import utils


class Syllabizer():
    """
    Syllabizer class. Takes care of download, processing and generation
    of all the data needed to make custom dictionaries
    """

    def __init__(self, lang):
        self.lang = lang
        self.raw = None
        self.words = None
        self.syllables = None

    def download_raw(self):
        """
        downloads a dictionary file from: https://github.com/brisvag/dictionaries
        """
        baseurl = 'https://raw.githubusercontent.com/brisvag/dictionaries/master/dictionaries/'

        print(f'Downloading raw data for "{self.lang}"...')
        # certifi is needed for mac, otherwise it complains about missing ssl certificates
        file = urlopen(f"{baseurl}/{self.lang}/index.dic", cafile=certifi.where())
        # need to wait a bit, cause files may be large. TODO: any better solution?
        sleep(3)

        self.raw = file

    def download_words(self):
        """
        downloads pregenerated word lists from: https://github.com/brisvag/gibberify-data
        """
        baseurl = 'https://raw.githubusercontent.com/brisvag/gibberify-data/master/words/'

        print(f'Downloading pregenerated words for "{self.lang}"...')
        # certifi is needed for mac, otherwise it complains about missing ssl certificates
        file = urlopen(f"{baseurl}/{self.lang}.json", cafile=certifi.where())
        # need to wait a bit, cause files may be large. TODO: any better solution?
        sleep(3)

        self.words = json.load(file)

    def download_syllables(self):
        """
        downloads pregenerated syllables from: https://github.com/brisvag/gibberify-data
        """
        baseurl = 'https://raw.githubusercontent.com/brisvag/gibberify-data/master/syllables/'

        print(f'Downloading pregenerated syllables for "{self.lang}"...')
        # certifi is needed for mac, otherwise it complains about missing ssl certificates
        file = urlopen(f"{baseurl}/{self.lang}.json", cafile=certifi.where())
        # need to wait a bit, cause files may be large. TODO: any better solution?
        sleep(3)

        self.syllables = json.load(file)

    def load_words(self):
        """
        loads word list from file
        """
        self.words = utils.access_data('words', self.lang)

    def load_syllables(self):
        """
        loads syllable list from file
        """
        self.syllables = utils.access_data('syllables', self.lang)

    def make_words(self):
        """
        parses a dictionary file-object in hunspell format (utf-8 version)

        returns a unique list of words
        """
        words = set()

        lines = self.raw.readlines()[1:]
        for line in lines:
            # decode and remove comments
            line = line.decode('utf-8').partition('/')[0]
            # strip line from unwanted stuff
            line = line.strip()
            # transliterate line if needed
            if self.lang in get_available_language_codes():
                line = translit(line, self.lang, reversed=True)
            # discard lines containing superscript/subscript
            if any(x in line for x in '⁰¹²³⁴⁵⁶⁷⁸⁹'):
                continue
            # discard lines containing non-alpha characters and with non-normal capitalization (acronyms...)
            if not line.isalpha() or (len(line) > 1 and not line[1:].islower()):
                continue
            words.add(line)

        # need to transform in list be able to save it as json
        words.discard('')

        self.words = list(words)

    def make_syllables(self):
        """
        generates a pool of syllables for a given language starting from a word list
        """
        syllables = set()

        print(f'Generating syllables for "{self.lang}"...')

        # open words file and syllabize all of them
        words = utils.access_data('words', self.lang)
        for word in words:
            # let's clean up once more just to be sure
            word = word.strip()
            syllables.update(set(utils.syllabize(word)))

        # # divide per length
        # syllables.discard('')
        # syl_dict = {}
        # for s in syllables:
        #     ln = len(s)
        #     if ln not in syl_dict.keys():
        #         syl_dict[ln] = []
        #     syl_dict[ln].append(s)
        #
        # utils.access_data('syllables', lang, write_data=syl_dict)

        self.syllables = list(syllables)

    def write(self, raw=False, words=False, syllables=True):
        """
        writes to file the generated data. If params are set to False, ignores that
        type of data when saving to file
        """
        if raw:
            utils.access_data('raw', self.lang, write_data=self.raw)
        if words:
            utils.access_data('words', self.lang, write_data=self.words)
        if syllables:
            utils.access_data('syllables', self.lang, write_data=self.syllables)

    def run(self, from_raw, force):
        """
        automatically downloads and parses data, then generates syllable pools
        :param from_raw: if True, download raw dictionaries and process everything locally
        :param force: if True, re-generate syllables even if already present
        """
        file = utils.clean_path(utils.data, 'syllables', f'{self.lang}.json')
        if not os.path.isfile(file) or force:
            if from_raw:
                self.download_raw()
                self.make_words()
                self.make_syllables()
            else:
                self.download_syllables()
            self.write()
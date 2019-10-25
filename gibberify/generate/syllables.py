# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

from urllib.request import urlopen
from transliterate import translit, get_available_language_codes
import json
import pickle
import certifi

# local imports
from .. import utils


class GibPool(list):
    """
    dict class that represents a pool of words or syllables of a specific language
    """
    def __init__(self, lang, *args, **kwargs):
        super(GibPool, self).__init__(*args, **kwargs)
        self.lang = lang
        self.version = utils.__version__


class Syllabizer:
    """
    Syllabizer class. Takes care of download, processing and generation
    of all the data needed to make custom dictionaries
    """
    def __init__(self, lang):
        self.lang = lang
        self.raw = None
        self.words = None
        self.syllables = None

    def _download_raw(self):
        """
        downloads a dictionary file from: https://github.com/brisvag/dictionaries
        """
        baseurl = 'https://raw.githubusercontent.com/brisvag/dictionaries/master/dictionaries/'

        print(f'Downloading raw data for {utils.r_lang_codes[self.lang]}...')
        # certifi is needed for mac, otherwise it complains about missing ssl certificates
        file = urlopen(f"{baseurl}/{self.lang}/index.dic", cafile=certifi.where())

        lines = file.readlines()[1:]
        return lines

    def _download_words(self):
        """
        downloads pregenerated word lists from: https://github.com/brisvag/gibberify-data
        """
        baseurl = 'https://raw.githubusercontent.com/brisvag/gibberify-data/master/words/'

        print(f'Downloading pregenerated words for {utils.r_lang_codes[self.lang]}...')
        # certifi is needed for mac, otherwise it complains about missing ssl certificates
        file = urlopen(f"{baseurl}/{self.lang}.p", cafile=certifi.where())

        return pickle.load(file)

    def _download_syllables(self):
        """
        downloads pregenerated syllables from: https://github.com/brisvag/gibberify-data
        """
        baseurl = 'https://raw.githubusercontent.com/brisvag/gibberify-data/master/syllables/'

        print(f'Downloading pregenerated syllables for {utils.r_lang_codes[self.lang]}...')
        # certifi is needed for mac, otherwise it complains about missing ssl certificates
        file = urlopen(f"{baseurl}/{self.lang}.p", cafile=certifi.where())

        return pickle.load(file)

    def _load_words(self):
        """
        loads word list from file
        """
        return utils.access_data('words', self.lang)

    def _load_syllables(self):
        """
        loads syllable list from file
        """
        return utils.access_data('syllables', self.lang)

    def _make_words(self):
        """
        parses a dictionary file-object in hunspell format (utf-8 version)

        :return: a unique list of words
        """
        words = set()

        lines = self.raw
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

        words.discard('')

        return GibPool(self.lang, words)

    def _make_syllables(self, from_file=False):
        """
        generates a pool of syllables for a given language starting from a word list
        :param from_file: load words from file instead of downloading them
        """
        syllables = set()

        print(f'Generating syllables for {utils.r_lang_codes[self.lang]}...')

        # open words file and syllabize all of them
        if from_file:
            words = utils.access_data('words', self.lang)
        else:
            words = self.words
        for word in words:
            # let's clean up once more just to be sure
            word = word.strip()
            syllables.update(set(utils.syllabize(word)))

        return GibPool(self.lang, syllables)

    def _write(self, words=False, syllables=True):
        """
        writes to file the generated data. If params are set to False, ignores that
        type of data when saving to file
        """
        if words:
            utils.access_data('words', self.lang, write_data=self.words)
        if syllables:
            utils.access_data('syllables', self.lang, write_data=self.syllables)

    def run(self, from_raw=False, download_words=False, from_words=False, force_rebuild=False):
        """
        automatically downloads and parses data, then generates syllable pools
        :param from_raw: if True, download raw dictionaries and process everything locally
        :param download_words: if True, download words instead of using the local files
        :param from_words: if True, download pre-generated word list and generate syllables from them
        :param force_rebuild: if True, re-generate or re-download syllables even if already present
        """
        file = utils.data/'syllables'/f'{self.lang}.p'
        if any((not file.is_file(), from_raw, download_words, from_words, force_rebuild)):
            if from_raw:
                self.raw = self._download_raw()
                self.words = self._make_words()
                self.syllables = self._make_syllables()
            elif download_words:
                self.words = self._load_words()
                self.syllables = self._make_syllables()
            elif from_words:
                self.words = self._download_words()
                self.syllables = self._make_syllables()
            else:
                self._download_syllables()

            # write data only if we have it
            self._write(words=bool(self.words), syllables=bool(self.syllables))

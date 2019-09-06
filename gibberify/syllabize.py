# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Download, parse and build all the data files needed by gibberify to do its magic
"""

from urllib.request import urlopen
from transliterate import translit, get_available_language_codes
from collections import OrderedDict
import pyphen
import certifi
from time import sleep
import os

# local imports
from . import utils
from . import config


def get_dict(lang):
    """
    downloads a dictionary file from: https://github.com/brisvag/dictionaries

    returns file object ready to be read
    """
    baseurl = 'https://raw.githubusercontent.com/brisvag/dictionaries/master/dictionaries/'

    print(f'Downloading "{lang}"...')
    # certifi is needed for mac, otherwise it complains about missing ssl certificates
    file = urlopen(f"{baseurl}/{lang}/index.dic", cafile=certifi.where())
    # need to wait a bit, cause files may be large. TODO: any better solution?
    sleep(3)

    return file


def get_words(lang, file_obj):
    """
    reads a dictionary file-object in hunspell format (utf-8 version)

    returns a cleaned up set of words
    """
    words = set()

    lines = file_obj.readlines()[1:]
    for line in lines:
        # decode and remove comments
        line = line.decode('utf-8').partition('/')[0]
        # strip line from unwanted stuff
        line = line.strip()
        # transliterate line if needed
        if lang in get_available_language_codes():
            line = translit(line, lang, reversed=True)
        # discard lines containing superscript/subscript
        if any(x in line for x in '⁰¹²³⁴⁵⁶⁷⁸⁹'):
            continue
        # discard lines containing non-alpha characters and with non-normal capitalization (acronyms...)
        if not line.isalpha() or (len(line) > 1 and not line[1:].islower()):
            continue
        words.add(line)

    # need to transform in list be able to save it as json
    words.discard('')
    words = list(words)

    return words


def download_data(lang):
    """
    downloads, cleans up and saves a word list for a language

    returns nothing
    """
    # download raw data
    raw = get_dict(lang)
    # get clean list of words from raw data
    words = get_words(lang, raw)
    # save it as json
    utils.access_data('words', lang, write_data=words)


def syllabize(word, hyph_list):
    """
    takes a word and reduces it to fundamental syllables using a list of
    pyphen hyphenators from several different languages

    returns a set of syllables
    """
    word = word.lower()

    # first get rid of apostrophes and such by splitting the word in sub-words
    syl = word.split('\'')
    for hyph in hyph_list:
        # do some list comprehension black magic to split up everything nicely
        syl = [s for w in syl for s in hyph.inserted(w).strip().split('-')]

    # nice trick to maintain order
    syllables = list(OrderedDict.fromkeys(syl))

    return syllables


def super_hyphenator():
    """
    returns a list of pyphen.Pyphen instances for each passed language
    """
    conf = config.import_conf()
    return [pyphen.Pyphen(lang=hyph_lang) for hyph_lang in conf['real_langs']]


def gen_syllables(conf, lang):
    """
    generates a pool of syllables for a given language starting from a word list in a file and
    saves to file a dictionary containing the syllables divided by length

    returns nothing
    """
    syllables = set()

    print(f'Generating syllables for "{lang}"...')

    # hyphen using a bunch of languages. This ensures we cut down syllables to the most fundamental ones
    # TODO: using pyphen.LANGUAGES is kinda overkill, reverting back to using the real_langs list
    hyph_list = super_hyphenator()

    # open words file and syllabize all of them
    words = utils.access_data('words', lang)
    for word in words:
        # let's clean up once more just to be sure
        word = word.strip()
        syllables.update(set(syllabize(word, hyph_list)))

    # divide per length
    syllables.discard('')
    syl_dict = {}
    for s in syllables:
        ln = len(s)
        if ln not in syl_dict.keys():
            syl_dict[ln] = []
        syl_dict[ln].append(s)

    utils.access_data('syllables', lang, write_data=syl_dict)


def build_syllables(download=False, langs=False):
    """
    builds a syllable pool for all the required languages, saves it as a file

    returns nothing
    """
    conf = config.import_conf()

    # check if languages in config.py exist in pyphen
    for l in conf['real_langs']:
        if l not in pyphen.LANGUAGES:
            raise KeyError(f'the language "{l}" is not supported by pyphen. Remove it from the configuration')

    # make sure data directories exist
    dirs = [
        utils.clean_path(utils.data, 'words'),
        utils.clean_path(utils.data, 'syllables'),
    ]
    for d in dirs:
        if not os.path.exists(d):
            os.makedirs(d)

    # main loop through languages
    for lang in conf['real_langs']:
        # only download again if requested or if local word lists are not present
        dw = download
        if not os.path.isfile(utils.clean_path(utils.data, 'words', f'{lang}.json')):
            dw = True
        if dw:
            download_data(lang)

        # generate syllables and save them, restricting to some languages if required
        if langs:
            if lang not in langs:
                print(f'Language "{lang}" will be skipped as requested.')
                continue
        gen_syllables(conf, lang)


if __name__ == '__main__':
    build_syllables()

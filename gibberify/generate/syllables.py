# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Download, parse and build all the data files needed by gibberify to do its magic
"""

from urllib.request import urlopen
from transliterate import translit, get_available_language_codes
import certifi
from time import sleep
import os

# local imports
from .. import utils


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


def gen_syllables(lang):
    """
    generates a pool of syllables for a given language starting from a word list in a file and
    saves to file a dictionary containing the syllables divided by length

    returns nothing
    """
    syllables = set()

    print(f'Generating syllables for "{lang}"...')

    # open words file and syllabize all of them
    words = utils.access_data('words', lang)
    for word in words:
        # let's clean up once more just to be sure
        word = word.strip()
        syllables.update(set(utils.syllabize(word)))

    # divide per length
    syllables.discard('')
    syl_dict = {}
    for s in syllables:
        ln = len(s)
        if ln not in syl_dict.keys():
            syl_dict[ln] = []
        syl_dict[ln].append(s)

    utils.access_data('syllables', lang, write_data=syl_dict)


def build_syllables(langs, force_download=False, force_generation=False):
    """
    builds a syllable pool for all the required languages if missing and saves it as a file

    download of words and syllable generation can both be forced even if files are present

    returns nothing
    """
    for lang in langs:
        # only download again if requested or if local word lists are not present
        words_file = utils.clean_path(utils.data, 'words', f'{lang}.json')
        if not os.path.isfile(words_file) or force_download:
            download_data(lang)

        # generate syllables and save them if they don't exist or if generation is force
        syl_file = utils.clean_path(utils.data, 'syllables', f'{lang}.json')
        if not os.path.isfile(syl_file) or force_generation:
            gen_syllables(lang)

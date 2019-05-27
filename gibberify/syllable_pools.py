from urllib.request import urlopen
import json
import pyphen
import re
from time import sleep


def import_dicts(lang_list):
    """
    downloads dictionary files from: https://github.com/wooorm/dictionaries

    returns a list of file objects ready to be read
    """
    files = {}

    baseurl = 'https://raw.githubusercontent.com/wooorm/dictionaries/master/dictionaries/'
    for lang in lang_list:
        print(f'Downloading "{lang}"...')
        file = urlopen(f"{baseurl}/{lang}/index.dic")
        # need to wait a bit, cause files may be large
        sleep(10)
        files[lang] = file

    return files


def get_words(file):
    """
    reads a dictionary file in hunspell format (utf-8 version)

    returns a set of words
    """
    words = set()

    # skip first line, header
    lines = file.readlines()[1:]
    for l in lines:
        # decode and remove comments
        l = l.decode('utf-8').partition('/')[0]
        # only use non-empty lines
        if l:
            words.add(l)

    return words


def gen_syllables(words, lang):
    """
    splits all the words in a given set into syllables using Italian
    as hyphenation language (see readme for why)

    returns all the usable syllables in a new set
    """
    syllables = set()

    print(f'Generating syllables for language: "{lang}"...')

    hyph = pyphen.Pyphen(lang='it')
    for w in words:
        # hyphenate and split into list
        syl = hyph.inserted(w).split('-')
        for s in syl:
            # clean up syllables from non-alpha characters
            s_clean = ''.join(c for c in s if c.isalpha())
            # remove syllables which contain uppercase letters after the first
            # (acronyms, other aberrations)
            if s_clean[1:].islower():
                # keep syllable only if it is between 2 and 5 characters and if they contain
                # vowels. This is to ensure usability for random word generation without
                # being unpronounceable or too recognizable. This is particularly relevant for
                # English, which has ridiculously dumb hyphenation rules.
                vowels = re.compile("[AEIOUYaeiouy]")
                if 2 <= len(s_clean) <= 4 and vowels.search(s_clean):
                    syllables.add(s_clean.lower())

    return syllables


def gen_pool(lang_list):
    """
    generates a dictionary with languages as keys and a set of syllables as values
    """
    pool = {}

    files = import_dicts(lang_list)
    for lang in files:
        # load words from the file
        words = get_words(files[lang])
        # get language string only, without locale
        lang = lang.split('-')[0]
        syllables = gen_syllables(words, lang)
        pool[lang] = list(syllables)

    return pool


if __name__ == '__main__':
    pool = gen_pool(['en-GB', 'it', 'de', 'fr', 'ru'])
    with open('syllables.json', 'w') as outfile:
        json.dump(pool, outfile, indent=1)

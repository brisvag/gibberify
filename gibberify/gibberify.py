# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Where the translation actually happens
"""

import re
import random

# local imports
from . import utils
from . import config
from .syllabize import super_hyphenator, syllabize


def gibberify(translator, text):
    """
    translate a text from real language into a specified gibberish language
    """
    # split words maintaining non-word characters in the right positions
    words = re.split(r'(\W+)(\w+)', text)

    # generate translation based on syllables
    trans_list = []
    # use syllabize to break down into syllables
    hyph_list = super_hyphenator(config.real_langs)
    for w in words:
        # leave non-word parts of the sentence as is
        if re.match(r'\w+', w):
            syl = syllabize(w, hyph_list)
            # check for translation in corresponding length
            # translate syllables only if they are found, otherwise return a random one
            trans_syl = [translator[str(len(s))].get(s.lower(), random.choice(list(translator[str(len(s))].keys())))
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

    return trans


def interactive():
    """
    interactive mode. Deal with user input and call functions accordingly
    """

    # Make it a sort of menu for easier usage
    level = 0
    while True:
        try:
            if level == 0:
                # welcome and usage
                print(f'Welcome to Gibberify {utils.version}! '
                      f'Follow the prompts to translate a text.\n'
                      f'To go back to the previous menu, press Ctrl+C.\n')
                level += 1
                continue

            if level == 1:
                lang_in = lang_out = ''

                # language selection
                while not lang_in:
                    lang_in = input(f'What language do you want to translate from? '
                                    f'Options are: {", ".join(config.real_langs)}.\n')
                    # check if requested input language exists
                    if lang_in not in config.real_langs:
                        print(f'ERROR: you first need to generate a syllable pool for "{lang_in}"!')
                        lang_in = ''
                    else:
                        lang_in = lang_in
                        print(f'You chose "{lang_in}".')
                while not lang_out:
                    lang_out = input(f'What language do you want to translate into? '
                                     f'Options are: {", ".join(list(config.gib_langs.keys()))}.\n')
                    # check if requested output language exists
                    if lang_out not in config.gib_langs:
                        print(f'ERROR: you first need to generate a dictionary for "{lang_out}"!')
                        lang_out = ''
                    else:
                        lang_out = lang_out
                        print(f'You chose "{lang_out}".')
                level += 1
                continue

            if level == 2:
                translator = utils.access_data('dicts', lang_in, lang_out)
                text = input('What do you want to translate?\n')
                print(f'... or, as someone might say:\n'
                      f'{gibberify(translator, text)}')
                continue

        except KeyboardInterrupt:
            level -= 1
            # exit the program if user tries to go back to level 0
            if level < 1:
                print('\nGood bye!\n')
                return
            print('\nGoing back...\n')
            continue

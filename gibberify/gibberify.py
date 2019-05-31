import json
import re
import pyphen
import random

# local imports
from utils import __version__
from config import real_langs, gib_langs


def gibberify(translator, text):
    """
    translate a text from real language into a specified gibberish language
    """
    # split words maintaining non-word characters in the right positions
    words = re.split(r'(\W+)(\w+)', text)

    # generate translation based on syllables
    trans_list = []
    hyph = pyphen.Pyphen(lang='it')
    for w in words:
        if re.match(r'\w+', w):
            syl = hyph.inserted(w).split('-')
            # translate syllables only if they are found, otherwise return a random one
            trans_syl = [translator.get(s.lower(), random.choice(list(translator.keys())))
                         for s in syl]
            # save word translation
            trans_w = ''.join(trans_syl)
            # let's preserve capitalisation, at least a bit
            if w[0].isupper():
                if w.isupper():
                    trans_w = trans_w.upper()
                else:
                    trans_w = trans_w.capitalize()
        else:
            # if w is not a word, just leave it as is
            trans_w = w

        trans_list.append(trans_w)

    # join everything
    trans = ''.join(trans_list)

    # remove multiple spaces due to input or unmapped syllables
    trans = re.sub(' +', ' ', trans)

    # TODO: strip ugly whitespaces and capitalise first letter in a smart way

    return trans


def interactive():
    """
    deal with user input and call functions accordingly
    """

    # Make it a sort of menu for easier usage
    level = 0
    while True:
        try:
            if level == 0:
                # welcome and usage
                print(f'Welcome to Gibberify version {__version__}! '
                      f'Follow the prompts to translate a text.\n'
                      f'To go back to the previous menu, press Ctrl+C.\n')
                level += 1
                continue

            if level == 1:
                lang_in = lang_out = ''

                # language selection
                while not lang_in:
                    lang_in = input(f'What language do you want to translate from? '
                                    f'Options are: {", ".join(real_langs)}.\n')
                    # check if requested input language exists
                    if lang_in not in real_langs:
                        print(f'ERROR: you first need to generate a syllable pool for "{lang_in}"!')
                        lang_in = ''
                    else:
                        print(f'You chose "{lang_in}".')
                while not lang_out:
                    lang_out = input(f'What language do you want to translate into? '
                                     f'Options are: {", ".join(gib_langs)}.\n')
                    # check if requested output language exists
                    if lang_out not in gib_langs:
                        print(f'ERROR: you first need to generate a dictionary for "{lang_out}"!')
                        lang_out = ''
                    else:
                        print(f'You chose "{lang_out}".')
                level += 1
                continue

            if level == 2:
                translator = dicts[lang_in][lang_out]
                text = input('What do you want to translate?\n')
                print(f'... or as someone might say:\n'
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

import argparse

def main():
    # Parse arguments (also gives you help automatically with -h)
    parser = argparse.ArgumentParser()
    parser.add_argument('--from-lang','-fl', dest='lang_in', type=str, default='en', choices=real_langs)
    parser.add_argument('--to-lang','-l', dest='lang_out', type=str, default='orc', choices=gib_langs.keys())
    parser.add_argument('--message', '-m', type=str)
    args = parser.parse_args()
    lang_in = args.lang_in
    lang_out = args.lang_out
    text = args.message

    # load translation dictionaries
    with open('../data/dicts.json') as f:
        global dicts
        dicts = json.load(f)

    if text:
        translator = dicts[lang_in][lang_out]
        print(gibberify(translator, text))
    else:
        interactive()


if __name__ == '__main__':
    main()

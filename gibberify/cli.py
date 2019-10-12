# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Command line interface and argument parsing
"""

import os
import sys
import argparse

# local imports. Here, they MUST actually be explicit, otherwise pyinstaller complains
from gibberify import utils
from gibberify import config
from gibberify.generate import build
from gibberify.translate import gibberify, direct_translator, gui


def parse():
    """
    provides a nice usage description and parses command line arguments

    returns namespace containing named arguments
    """
    # Parse arguments (also gives you help automatically with -h)
    parser = argparse.ArgumentParser(prog='gibberify', formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Gibberify is simple gibberish generator.\n'
                                                 'Run without arguments to use the graphical interface.',
                                     add_help=False)

    gen_opt = parser.add_argument_group('utils options')
    gen_opt.add_argument('-i', '--interactive', dest='inter', action='store_true',
                         help='run in interactive mode')
    gen_opt.add_argument('-h', '--help', action='help',
                         help='show this help message and exit')
    gen_opt.add_argument('-V', '--version', action='store_true',
                         help='display version information and exit')

    trans_opt = parser.add_argument_group('translation options')
    trans_opt.add_argument('-f', '--from', dest='lang_in', type=str, default='en',
                           help='language to translate from')
    trans_opt.add_argument('-t', '--to', dest='lang_out', type=str, default='orc',
                           help='language to translate into')
    trans_opt.add_argument('-m', '--message', type=str, nargs='*',
                           help='text to translate. If a filename is given, the '
                                'contents of the file will be translated to stdout. '
                                'If `-` is given, input text is take from stdin. '
                                'Question marks are not supported')

    build_opt = parser.add_argument_group('configuration and building options')
    build_opt.add_argument('--config', dest='config', action='store_true',
                           help='open configuration file for editing, then rebuild dictionaries accordingly')
    build_opt.add_argument('--force-download', dest='force_download', action='store_true',
                           help='force re-download of word data, creation of syllable pools and generation of '
                                'dictionary files for all the language combinations.')
    build_opt.add_argument('--force-syllables', dest='force_syllables', action='store_true',
                           help='force re-generation of syllable pools and dictionary files '
                                'for all the language combinations.')
    build_opt.add_argument('--rebuild-dicts', dest='rebuild_dicts', action='store_true',
                           help='rebuild translation dictionaries. Use this option '
                                'after changing dictionary generation settings')

    return parser.parse_args()


def interactive():
    """
    interactive mode. Deal with user input and call functions accordingly
    """
    conf = config.import_conf()
    real_langs = conf['real_langs']
    gib_langs = conf['gib_langs'].keys()

    # TODO: add support for reverse translation
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
                                    f'Options are: {", ".join(real_langs)}.\n')
                    # check if requested input language exists
                    if lang_in not in real_langs:
                        print(f'ERROR: you first need to generate a syllable pool for "{lang_in}"!')
                        lang_in = ''
                    else:
                        lang_in = lang_in
                        print(f'You chose "{lang_in}".')
                while not lang_out:
                    lang_out = input(f'What language do you want to translate into? '
                                     f'Options are: {", ".join(gib_langs)}.\n')
                    # check if requested output language exists
                    if lang_out not in gib_langs:
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


def dispatch(args):
    """
    takes namespace with named arguments and based on them dispatches to the right modules
    """
    if args.version:
        print(f'Gibberify {utils.version}')
        sys.exit()

    # if no arguments were given, run gui version
    graphical = True if len(sys.argv) == 1 else False

    conf = config.import_conf()

    if args.config:
        config.edit_conf()

    if args.force_download or args.force_syllables or args.rebuild_dicts or args.config:
        build(force_syllables=args.force_syllables, force_download=args.force_download)
        sys.exit()

    # before running anything, check if data files exist and create them if needed
    for real_lang, gib_lang in zip(conf['real_langs'], conf['gib_langs']):
        straight = utils.clean_path(utils.data, 'dicts', f'{real_lang}-{gib_lang}.json')
        reverse = utils.clean_path(utils.data, 'dicts', f'{gib_lang}-{real_lang}.json')
        if not any([os.path.isfile(straight), os.path.isfile(reverse)]):
            print('Dictionaries are missing! I will generate all the data first. It may take a minute!\n')
            build()
            break

    # dispatch
    if graphical:
        gui()
    elif args.inter:
        interactive()
    else:
        print(direct_translator(args.lang_in, args.lang_out, ' '.join(args.message)))


def main():
    # get arguments
    args = parse()
    # dispatch to correct function based on arguments
    dispatch(args)

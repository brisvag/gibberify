# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Command line interface and argument parsing
"""

import os
import sys
import argparse

# local imports
from . import utils
from .config import Config
from .generate import build
from .translate import Translator
from .ui import gui, interactive


def parse():
    """
    provides a nice usage description and parses command line arguments

    returns namespace containing named arguments
    """
    # TODO: add option to delete all config and data files (useful for uninstall)
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


def run(args):
    """
    takes namespace with named arguments and based on them control the main functions and modules of gibberify
    """
    if args.version:
        print(f'Gibberify {utils.version}')
        sys.exit()

    # if no arguments were given, run gui version
    graphical = True if len(sys.argv) == 1 else False

    conf = Config.from_json()

    if args.config:
        conf.edit()

    if args.force_download or args.force_syllables or args.rebuild_dicts or args.config:
        build(conf, from_raw=args.force_download, force_syl_rebuild=args.force_syllables,
              force_dicts_rebuild=args.rebuild_dicts)
        sys.exit()

    # before running anything, check if data files exist and create them if needed
    for real_lang in conf['real_langs']:
        for gib_lang in conf['gib_langs'].keys():
            straight = utils.data/'dicts'/f'{real_lang}-{gib_lang}.json'
            reverse = utils.data/'dicts'/f'{gib_lang}-{real_lang}.json'
            if not any([straight.is_file(), reverse.is_file()]):
                print('Dictionaries are missing! I will generate the missing data first. It may take a minute!\n')
                build(conf)
                break

    if not graphical and not args.inter:
        message = args.message[0]
        print(Translator(args.lang_in, args.lang_out, message))
    else:
        if graphical:
            gui()
        elif args.inter:
            interactive()
        else:
            raise NotImplementedError('How did you get here?')


def main():
    # get arguments
    args = parse()
    # dispatch to correct function based on arguments
    run(args)

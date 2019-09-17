# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Command line interface and argument parsing
"""

import os
import sys
import argparse

# local imports. Here, they MUST actually be explicit, otherwise pyinstaller complains
from . import utils
from . import config
from .syllabize import build_syllables
from .degibberify import build_all_dicts
from .gibberify import gibberify, interactive
from .gui import gui


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

    gen_opt = parser.add_argument_group('general options')
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
                           help='force re-download of word data and create syllable pools, then generate '
                                'dictionary files for all the language combinations.')
    build_opt.add_argument('--rebuild-dicts', dest='rebuild_dicts', action='store_true',
                           help='rebuild translation dictionaries. Use this option '
                                'after changing dictionary generation settings')

    return parser.parse_args()


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

    # do-something-and-exit arguments
    if args.config:
        config.edit_conf()
        build_all_dicts(force_rebuild=True)
        sys.exit()
    elif args.force_download:
        build_syllables(download=True)
        build_all_dicts(force_rebuild=True)
        sys.exit()
    elif args.rebuild_dicts:
        build_all_dicts(force_rebuild=True)
        sys.exit()

    # before running anything, check if data files exist and create them if needed
    for real_lang, gib_lang in zip(conf['real_langs'], conf['gib_langs']):
        straight = utils.clean_path(utils.data, 'dicts', f'{real_lang}-{gib_lang}.json')
        reverse = utils.clean_path(utils.data, 'dicts', f'{gib_lang}-{real_lang}.json')
        if not any([os.path.isfile(straight), os.path.isfile(reverse)]):
            print('Dictionaries are missing! I will generate all the data first. It may take a minute!\n')
            build_all_dicts(force_rebuild=True)
            break

    # dispatch
    if graphical:
        gui()
    elif args.inter:
        interactive()
    else:
        translator = utils.access_data('dicts', args.lang_in, args.lang_out)
        print(gibberify(translator, ' '.join(args.message)))


def main():
    # get arguments
    args = parse()
    # dispatch to correct function based on arguments
    dispatch(args)


if __name__ == '__main__':
    main()

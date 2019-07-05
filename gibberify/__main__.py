# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Main entry point of gibberify
"""

import sys
import argparse

# local imports. Here, they MUST actually be explicit, otherwise pyinstaller complains
from gibberify.utils import __version__, access_data, parse_message, is_standalone, data_exists
from gibberify.syllabize import build_syllables
from gibberify.scramble import build_dicts
from gibberify.degibberify import build_reverse_dicts
from gibberify.gibberify import gibberify, interactive
from gibberify.gui import gui


def main():
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
    trans_opt.add_argument('-m', '--message', type=parse_message, nargs='*',
                           help='text to translate. If a filename is given, the '
                                'contents of the file will be translated to stdout. '
                                'If `-` is given, input text is take from stdin. '
                                'Question marks are not supported')

    if not is_standalone():
        build_opt = parser.add_argument_group('building options')
        build_opt.add_argument('--force-download', dest='force_download', action='store_true',
                               help='force re-download of word data and create syllable pools, then generate '
                                    'dictionary files for all the language combinations. '
                                    'This may take a few minutes')
        build_opt.add_argument('--rebuild-syllables', dest='rebuild_syllables', action='store_true',
                               help='rebuild syllable pools, without downloading word lists. '
                                    'Then, generate dictionaries with the new syllables')
        build_opt.add_argument('--rebuild-dicts', dest='rebuild_dicts', action='store_true',
                               help='rebuild translation dictionaries only. Use this option '
                                    'after changing settings in config.py')

    args = parser.parse_args()

    if args.version:
        print(f'Gibberify {__version__}')
        exit()

    # if no arguments were given, run gui version
    graphical = False
    if len(sys.argv) == 1:
        graphical = True

    if not is_standalone():
        if args.force_download:
            build_syllables(download=True)
            build_dicts()
            build_reverse_dicts()
            exit()
        if args.rebuild_syllables:
            build_syllables(download=False)
            build_dicts()
            build_reverse_dicts()
            exit()
        if args.rebuild_dicts:
            build_dicts()
            build_reverse_dicts()
            exit()

    # before running anything, check if data file exist:
    if not data_exists():
        print('ERROR: Dictionaries are missing! Make sure to generate all the data first.\n')
        parser.print_usage()
        exit(1)

    if graphical:
        gui()
    elif args.inter:
        interactive()
    else:
        translator = access_data('dicts', args.lang_in, args.lang_out)
        print(gibberify(translator, ' '.join(args.message)))


if __name__ == '__main__':
    main()

"""
Main entry point of gibberify
"""

import os
import sys
import argparse
import json

# local imports
from .config import __real_langs__, __gib_langs__
from .utils import __version__, __data__
from .gibberify import gibberify, parse_message, interactive
from .gui import gui


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
    trans_opt.add_argument('-fl', '--from-lang', dest='lang_in', type=str, default='en',
                           help='language to translate from')
    trans_opt.add_argument('-l', '--to-lang', dest='lang_out', type=str, default='orc',
                           help='language to translate into')
    trans_opt.add_argument('-m', '--message', type=parse_message, nargs='*',
                           help='text to translate. If a filename is given, the '
                                'contents of the file will be translated to stdout. '
                                'If `-` is given, input text is take from stdin. '
                                'Question marks are not supported')
    args = parser.parse_args()

    if args.version:
        print(f'Gibberify {__version__}')
        exit()

    # if no arguments were given, run gui version
    graphical = False
    if len(sys.argv) == 1:
        graphical = True

    if graphical:
        gui()
    elif args.inter:
        interactive()
    else:
        with open(os.path.join(__data__, 'dicts', f'{args.lang_in}-{args.lang_out}.json'), 'r') as f:
            translator = json.load(f)
        print(gibberify(translator, ' '.join(args.message)))


if __name__ == '__main__':
    main()

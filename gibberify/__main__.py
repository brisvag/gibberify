"""
Main entry point of gibberify
"""

import os
import sys
import argparse
import json

# local imports
from .config import real_langs, gib_langs
from .gibberify import gibberify, parse_message, interactive
from .gui import gui

def main():
    # Parse arguments (also gives you help automatically with -h)
    parser = argparse.ArgumentParser(prog='gibberify')
    parser.add_argument('--interactive', '-i', dest='inter', action='store_true',
                        help='run in interactive mode')
    parser.add_argument('--from-lang', '-fl', dest='lang_in', type=str, default='en',
                        choices=real_langs, help='language to translate from')
    parser.add_argument('--to-lang', '-l', dest='lang_out', type=str, default='orc',
                        choices=gib_langs.keys(), help='language to translate into')
    parser.add_argument('--message', '-m', type=parse_message, nargs='*',
                        help='text to translate. If a filename is given, the '
                             'contents of the file will be translated to stdout. '
                             'If `-` is given, input text is take from stdin')
    args = parser.parse_args()

    # if no arguments were given, run gui version
    graphical = False
    if len(sys.argv) == 1:
        graphical = True

    # fix path to files depending if we are running as script or as executable
    if hasattr(sys, "_MEIPASS"):
        data = os.path.join(sys._MEIPASS, 'data')
    else:
        data = os.path.join(os.path.dirname(__file__), 'data')

    # load translation dictionaries
    with open(os.path.join(data, 'dicts.json')) as f:
        dicts = json.load(f)

    if graphical:
        gui(dicts)
    elif args.inter:
        interactive(dicts)
    else:
        translator = dicts[args.lang_in][args.lang_out]
        print(gibberify(translator, ' '.join(args.message)))


if __name__ == '__main__':
    main()

"""
Collection of utilities and globals
"""

import os
import sys
import json

__version__ = 0.1


if hasattr(sys, "_MEIPASS"):
    __data__ = os.path.join(sys._MEIPASS, 'data')
else:
    __data__ = os.path.join(os.path.dirname(__file__), 'data')


def code(lang):
    """
    strips locale info from language

    returns 2-letter code
    """
    return lang.split('-')[0]


def progress(message, partial, total):
    """
    print progress in percentage with carriage return
    """
    # +0.5 is to round up
    print(f'\r{message}: {int((partial/total)*100+0.5)}%', flush=True, end='')


def access_data(data_type, real_lang, gib_lang=None, write_data=None):
    """
    utility function to load or write data files
    """
    if data_type not in ['words', 'syllables', 'dicts']:
        raise ValueError(f'no such data type as "{data_type}"')

    real_lang = code(real_lang)
    dest = real_lang
    if gib_lang:
        gib_lang = code(gib_lang)
        dest = f'{real_lang}-{gib_lang}'
    mode = 'r'
    if write_data:
        mode = 'w+'

    with open(os.path.join(__data__, data_type, f'{dest}.json'), mode) as f:
        if not write_data:
            return json.load(f)
        else:
            json.dump(write_data, f, indent=2)


def parse_message(somestring):
    """
    Handle message input nicely
    Passing '-' as the message will read from stdin
    Passing a valid file will read from the file
    Passing a string will use it as the message.
    If your string happens to accidentally be a valid file,
    tough shit i guess..
    """
    somestring = str(somestring)
    if somestring == '-':
        try:
            return sys.stdin.read()
        except KeyboardInterrupt:
            print()
            exit()
    elif os.path.exists(somestring):
        with open(somestring, 'r') as f:
            return f.read()
    else:
        return somestring

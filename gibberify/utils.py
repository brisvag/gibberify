# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Collection of utilities and globals
"""

import os
import sys
import json

# local imports
from .config import __real_langs__, __gib_langs__

__version__ = 0.1


def is_standalone():
    """
    check whethere it's runnin gin standalone mode

    returns true or false
    """
    if hasattr(sys, "_MEIPASS"):
        return True
    return False


# TODO: refactor these functions into one that returns package dir and
#       if possible use pkg_resources for standalone
def find_data():
    if is_standalone():
        return os.path.join(sys._MEIPASS, 'data')
    else:
        return os.path.join(os.path.dirname(__file__), 'data')


def find_assets():
    if is_standalone():
        return os.path.join(sys._MEIPASS, 'assets')
    else:
        return os.path.join(os.path.dirname(__file__), 'assets')


def find_config():
    if is_standalone():
        return os.path.join(sys._MEIPASS, 'config.py')
    else:
        return os.path.join(os.path.dirname(__file__), 'config.py')


__data__ = find_data()
__assets__ = find_assets()


def progress(message, partial, total):
    """
    print progress in percentage with carriage return
    """
    # +0.5 is to round up
    print(f'\r{message}: {int((partial/total)*100+0.5)}%', flush=True, end='')


def access_data(data_type, lang_in, lang_out=None, write_data=None):
    """
    utility function to load or write data files
    """
    if data_type not in ['words', 'syllables', 'dicts']:
        raise ValueError(f'no such data type as "{data_type}"')

    dest = lang_in
    if lang_out:
        dest = f'{dest}-{lang_out}'
    mode = 'r'
    if write_data:
        mode = 'w+'

    with open(os.path.join(__data__, data_type, f'{dest}.json'), mode) as f:
        if not write_data:
            return json.load(f)
        else:
            json.dump(write_data, f, indent=2)


def data_exists():
    """
    make sure all the dict files required for translation exist
    """
    for real_lang in __real_langs__:
        for gib_lang in __gib_langs__:
            straight = os.path.join(__data__, 'dicts', f'{real_lang}-{gib_lang}.json')
            reverse = os.path.join(__data__, 'dicts', f'{gib_lang}-{real_lang}.json')
            if not any([os.path.isfile(straight), os.path.isfile(reverse)]):
                return False
    return True


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
    elif os.path.isfile(somestring):
        with open(somestring, 'r') as f:
            return f.read()
    else:
        return somestring

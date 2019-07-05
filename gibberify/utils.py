# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Collection of utilities and globals
"""

import os
import sys
import json
import platform

# local imports
from .config import __real_langs__, __gib_langs__

# TODO: keep updated!
__version__ = 0.1


# TODO: is this needed anymore?
def is_standalone():
    """
    check whethere it's runnin gin standalone mode

    returns true or false
    """
    if hasattr(sys, "_MEIPASS"):
        return True
    return False


def clean_path(*steps):
    """
    joins strings into a path, then returns a cleaned up version with expanded variables and ~
    """
    path = os.path.realpath(os.path.expanduser(os.path.expandvars(os.path.join(*steps))))

    return path


def get_data_dir():
    """
    OS-sensitive function to find a good place to store data and config files
    """
    os_name = platform.system().lower()
    basedir = ''
    if os.name in ['linux', 'darwin']:
        basedir = clean_path('~', '.config')
    elif os_name == 'windows':
        try:
            basedir = clean_path(os.getenv('APPDATA'))
        except KeyError:
            print(f'ERROR: could not find "APPDATA" environment variable.')
            exit(0)

    datadir = clean_path(basedir, 'gibberify')

    return datadir


# TODO: refactor these functions into one that returns package dir and
#       if possible use pkg_resources for standalone
def find_assets():
    if is_standalone():
        return clean_path(sys._MEIPASS, 'assets')
    else:
        return clean_path(os.path.dirname(__file__), 'assets')


__data__ = get_data_dir()
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
        dest = f'{lang_in}-{lang_out}'
    mode = 'r'
    if write_data:
        mode = 'w+'

    with open(clean_path(__data__, data_type, f'{dest}.json'), mode) as f:
        if not write_data:
            return json.load(f)
        else:
            json.dump(write_data, f, indent=2)


def data_exists():
    """
    make sure all the dict files required for translation exist
    """
    for real_lang, gib_lang in zip(__real_langs__, __gib_langs__.keys()):
        straight = clean_path(__data__, 'dicts', f'{real_lang}-{gib_lang}.json')
        reverse = clean_path(__data__, 'dicts', f'{gib_lang}-{real_lang}.json')
        if not any([os.path.isfile(straight), os.path.isfile(reverse)]):
            return False
    return True


def parse_message(str_in):
    """
    Handle message input nicely
    Passing '-' as the message will read from stdin
    Passing a valid file will read from the file
    Passing a string will use it as the message.
    If your string happens to accidentally be a valid file,
    tough shit i guess..
    """
    # TODO: handle this a bit better (now only checks each word separately)
    str_in = str(str_in)
#    if str_in == '-':
#        try:
#            return sys.stdin.read()
#        except KeyboardInterrupt:
#            print()
#            exit()
#    elif os.path.isfile(str_in):
#        with open(str_in, 'r') as f:
#            return f.read()
#    else:
    return str_in

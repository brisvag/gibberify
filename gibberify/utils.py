# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Collection of utilities and globals
"""

import os
import sys
import json
import platform


# TODO: is this needed anymore?
def is_standalone():
    """
    check whether it's running in standalone mode

    returns true or false
    """
    if hasattr(sys, "_MEIPASS"):
        return True
    return False


def clean_path(*steps):
    """
    joins strings into a path, then returns a cleaned up version with expanded variables and ~
    """
    return os.path.realpath(os.path.expanduser(os.path.expandvars(os.path.join(*steps))))


def get_data_dir():
    """
    OS-sensitive function to find a good place to store data and config files
    """
    os_name = platform.system().lower()
    basedir = ''
    if os_name in ['linux', 'darwin']:
        basedir = clean_path('~', '.config')
    elif os_name == 'windows':
        try:
            basedir = clean_path(os.getenv('APPDATA'))
        except KeyError:
            print(f'ERROR: could not find "APPDATA" environment variable.')
            exit(0)
    datadir = clean_path(basedir, 'gibberify')
    return datadir


def find_basedir():
    if is_standalone():
        return clean_path(sys._MEIPASS)
    else:
        return clean_path(os.path.dirname(__file__))


def progress(message, partial, total):
    """
    print progress in percentage with carriage return
    """
    # TODO: use this!
    # +0.5 is to round up
    print(f'\r{message}: {int((partial/total)*100+0.5)}%', flush=True, end='')
    if partial == total:
        print()


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

    with open(clean_path(data, data_type, f'{dest}.json'), mode) as f:
        if not write_data:
            return json.load(f)
        else:
            json.dump(write_data, f, indent=4)


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


# initialize all the globals used by other modules
version = '0.3.0'

basedir = find_basedir()
assets = clean_path(basedir, 'assets')

data = get_data_dir()
conf = clean_path(data, 'config.json')

# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Collection of utilities and globals
"""

import os
import sys
import json
import platform


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
    """
    return path to module directory,
    """
    if hasattr(sys, "_MEIPASS"):
        return clean_path(sys._MEIPASS)     # needed for standalone version
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
# initialize all the globals used by other modules
version = '0.3.0'

basedir = find_basedir()
assets = clean_path(basedir, 'assets')

data = get_data_dir()
conf = clean_path(data, 'config.json')

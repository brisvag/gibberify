# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Collection of general utilities and globals used by several modules
"""

import os
import sys
import json
import platform
from pathlib import Path


def find_data_dir():
    """
    OS-sensitive function to find a good place to store data and config files
    """
    os_name = platform.system().lower()
    if os_name in ['linux', 'darwin']:
        conf_dir = Path('~/.config').expanduser()
    elif os_name == 'windows':
        try:
            conf_dir = Path(os.getenv('APPDATA')).expanduser()
        except KeyError:
            print(f'ERROR: could not find "APPDATA" environment variable.')
            exit(0)
    else:
        raise OSError('cannot detect OS correctly')
    datadir = conf_dir/'gibberify'
    return datadir


def find_basedir():
    """
    return path to module directory,
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).expanduser()     # needed for standalone version
    else:
        return Path(os.path.dirname(__file__)).parent


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
    :param data_type: type of data to access (raw, words, syllables or dicts)
    :param lang_in: (input) language code
    :param lang_out: output language code.
    :param write_data: data in json compatible format. If not present, data is read from file and returned instead
    :return: contents of the file in json compatible format, if any
    """
    if data_type == 'dicts':
        if not lang_out:
            raise AttributeError('you must specify an output language to access a dictionary')
        name = f'{lang_in}-{lang_out}'
    elif data_type in ('syllables', 'words', 'raw'):
        name = lang_in
    else:
        raise ValueError(f'no such data type as "{data_type}"')

    mode = 'r'
    if write_data:
        mode = 'w+'

    file_path = data/data_type/f'{name}.json'
    with open(file_path, mode) as f:
        if not write_data:
            return json.load(f)
        else:
            json.dump(write_data, f, indent=4)


# initialize all the globals used by other modules
version = '0.4.2'

basedir = find_basedir()
assets = basedir/'assets'

data = find_data_dir()
conf = data/'config.json'

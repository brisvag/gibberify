# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Collection of general utilities and globals used by several modules
"""

import os
import sys
from packaging import version
import pickle
import platform
import shutil
from pathlib import Path


class VersionError(Exception):
    """
    error raised when there's a version mismatch between loaded data and current version of gibberify
    """
    pass


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
    return path to module directory
    """
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS).expanduser()     # needed for standalone version
    else:
        return Path(os.path.dirname(__file__)).parent


def check_dirs():
    """
    create directory tree for data if not present
    """
    dirs = ['words', 'syllables', 'dicts']
    for d in dirs:
        path = data/d
        os.makedirs(path, exist_ok=True)


def access_data(data_type, lang_in, lang_out=None, write_data=None):
    """
    utility function to load or write data files
    :param data_type: type of data to access (raw, words, syllables or dicts)
    :param lang_in: (input) language code
    :param lang_out: output language code.
    :param write_data: data pickleable format. If not present, data is read from file and returned instead
    :return: contents of the file in pickleable format, if any
    """
    check_dirs()
    if data_type == 'dicts':
        if not lang_out:
            raise AttributeError('you must specify an output language to access a dictionary')
        name = f'{lang_in}-{lang_out}'
    elif data_type in ('syllables', 'words'):
        name = lang_in
    else:
        raise ValueError(f'no such data type as "{data_type}"')

    mode = 'rb'
    if write_data:
        mode = 'wb+'

    file_path = data/data_type/f'{name}.p'

    with open(file_path, mode) as f:
        if not write_data:
            loaded = pickle.load(f)
            v_load = version.parse(loaded.version).release
            v_curr = version.parse(__version__).release
            if v_load[0] < v_curr[0]:
                raise VersionError('loaded data is from an old, non compatible version')
            return loaded
        else:
            pickle.dump(write_data, f)


def uninstall(force=False):
    """
    deletes all the generated data and the user configuration
    """
    if not data.is_dir():
        print('There is nothing to uninstall!')
    else:
        if not force:
            confirm = ''
            while confirm not in ['y', 'n']:
                confirm = input('Are you sure? (y/n)')
            if confirm == 'n':
                return
        print('Removing all the generated data and custom configuration.')
        shutil.rmtree(data)


# initialize all the globals used by other modules
__version__ = '0.5.0'

basedir = find_basedir()
assets = basedir/'assets'
conf_default = basedir/'config'/'config.json'

data = find_data_dir()
conf = data/'config.json'

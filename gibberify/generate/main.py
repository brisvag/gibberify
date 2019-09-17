# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Main entry point of the dictionary generaction submodule
"""


import os
import pyphen

# local imports
from .. import utils
from .. import config
from .syllables import build_syllables
from .scramble import build_straight_dicts
from .unscramble import build_reverse_dicts


def check_pyphen(langs):
    """
    make sure all languages in the configuration are available in pyphen
    """
    for lang in langs:
        if lang not in pyphen.LANGUAGES:
            raise KeyError(f'the language "{lang}" is not supported by pyphen. Remove it from the configuration')


def check_dirs():
    """
    create directory tree for data if not present
    """
    dirs = ['words', 'syllables', 'dicts']
    for d in dirs:
        path = utils.clean_path(utils.data, d)
        os.makedirs(path, exist_ok=True)


def build(force_syllables=False, force_download=False):
    """
    generates all data required by gibberify to work
    """
    conf = config.import_conf()

    # preliminary checks
    check_pyphen(conf['real_langs'])
    check_dirs()

    # call functions
    build_syllables(conf['real_langs'], force_download=force_download, force_generation=force_syllables)
    build_straight_dicts(conf['real_langs'], conf['gib_langs'])
    build_reverse_dicts(conf['gib_langs'].keys(), conf['real_langs'])

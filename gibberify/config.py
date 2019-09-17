# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
This module takes care of customization through the use of a configuration file

config.json is strucutred as follows:

# natural languages used for syllable generation and everything else
# languages must be indicated with international 2-letter codes

real_langs = [
    "en",   # english
    ...
]

# gibberish languages and their relative settings
# language codes should be 3 letters long, to avoid conflict with real languages

gib_langs = {
    "orc": {
        "pool": ["ru", "de"],   # pool of languages to draw syllables from
        "notimplemented_setting": "something_awesome"
    },
    ...
}
"""

import os
import json
import texteditor
from time import sleep
import shutil

# local imports
from . import utils


def get_defaults():
    base_conf = utils.clean_path(utils.basedir, 'config.json')
    with open(base_conf, 'r') as f:
        return json.load(f)


def write_conf(conf):
    with open(utils.conf, 'w+') as f:
        json.dump(conf, f, indent=4)


def make_conf():
    """
    does nothing if config file exists, otherwise creates one
    """
    os.makedirs(utils.data, exist_ok=True)
    if not os.path.exists(utils.conf):
        conf = get_defaults()
        write_conf(conf)


def edit_conf():
    """
    opens the config file in the default editor
    """
    texteditor.open(filename=utils.conf)


def import_conf():
    """
    import user-defined configuration from data directory
    create a new one if not present
    """
    make_conf()

    try:
        with open(utils.conf, 'r') as f:
            return json.load(f)
    except json.decoder.JSONDecodeError:
        print('ERROR: your configuration file is corrupted!\n'
              'Try to fix it...')
        sleep(2)
        edit_conf()
    try:
        with open(utils.conf, 'r') as f:
            return json.load(f)
    except json.decoder.JSONDecodeError:
        print('ERROR: still corrupted. Backing up and resetting to defaults.')
        shutil.move(utils.conf, f'{utils.conf}.backup')
        make_conf()

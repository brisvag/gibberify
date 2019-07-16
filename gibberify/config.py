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

# local imports
from .utils import clean_path, __data__, __basedir__, __conf__


def make_conf():
    """
    does nothing if config file exists, otherwise creates one
    """
    if os.path.exists(__conf__):
        pass
    else:
        if not os.path.exists(__data__):
            os.makedirs(__data__)
        base_conf = clean_path(__basedir__, 'config.json')
        with open(base_conf, 'r') as f:
            conf = json.load(f)
        with open(__conf__, 'w+') as f:
            json.dump(conf, f, indent=4)


def edit_conf():
    """
    opens the config file in the default editor
    """
    return texteditor.open(filename=__conf__)


def import_conf():
    """
    import user-defined configuration from data directory
    create a new one if not present
    """
    make_conf()

    with open(__conf__, 'r') as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            print('ERROR: your configuration file is corrupted!\n'
                  'I will open it in an editor so you can fix it.')
            sleep(3)
            json.loads(edit_conf())
            exit(2)


conf = import_conf()
__real_langs__ = conf['real_langs']
__gib_langs__ = conf['gib_langs']

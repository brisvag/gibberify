# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
This module takes care of customization through the use of a configuration file

config.json is strucutred as follows:

# natural languages used for syllable generation and everything else
# languages must be indicated with international 2-letter codes
# add, remove or comment out lines to edit the base list

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

# local imports
from .utils import clean_path, __data__, __basedir__


def get_conf():
    """
    import user-defined configuration from data directory
    create a new one if not present
    """
    conf_path = clean_path(__data__, 'config.json')

    if not os.path.exists(__data__):
        os.makedirs(__data__)

    if os.path.isfile(conf_path):
        with open(conf_path, 'r') as f:
            conf = json.load(f)
    else:
        base_conf = clean_path(__basedir__, 'config.json')
        with open(base_conf, 'r') as f:
            conf = json.load(f)
        with open(conf_path, 'w+') as f:
            json.dump(conf, f, indent=4)

    return conf


conf = get_conf()
__real_langs__ = conf['real_langs']
__gib_langs__ = conf['gib_langs']
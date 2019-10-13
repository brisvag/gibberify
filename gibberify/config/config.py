# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
This module takes care of customization through the use of a configuration file

config.json is structured as follows:

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
        "pool": ["ru", "de"],       # pool of languages to draw syllables from
        "enrich": ["g", "k", "r"],  # get more of these in the target language
        "impoverish": ["w"],        # get less of these in the target language
        "remove": []                # get none of these in the target language
    },
    ...
}
"""

import json
import texteditor

# local imports
from .. import utils


class Config(dict):
    """
    Config class

    a modified dictionary class that can retrieve, store and edit the configuration for gibberify
    """
    default_path = utils.basedir / 'config' / 'config.json'
    user_path = utils.conf

    @classmethod
    def from_json(cls, path=None):
        """
        creates a config object starting from a json file
        :param path: path of the json file. If not given, default path for user config is used
        :return: Config instance
        """
        if not path:
            path = cls.user_path
        try:
            with open(path, 'r') as f:
                return cls(json.load(f))
        except FileNotFoundError:
            with open(cls.default_path, 'r') as f:
                return cls(json.load(f))

    @classmethod
    def from_default(cls):
        """
        wrapper for from_json that loads the default configuration
        """
        return cls.from_json(cls.default_path)

    def write(self):
        """
        writes the current configuration to file
        """
        with open(self.user_path, 'w+') as f:
            json.dump(self, f, indent=4)

    def edit(self):
        """
        opens the configuration file in the default text editor
        """
        texteditor.open(filename=self.user_path)

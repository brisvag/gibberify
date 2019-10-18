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


class ConfigError(Exception):
    """
    error raised by Config when provided with a wrong format or value
    """
    pass


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

    def check(self):
        """
        check that contents of the dictionary conform the format, try to fix it if not,
        otherwise raise an exception
        """
        def checktype(inst, itype):
            if not isinstance(inst, itype):
                raise TypeError(f'{type(inst)} should be {itype}')

        for key, value in self.items():
            if key == 'real_langs':
                checktype(value, list)
                for lang in value:
                    if lang not in utils.r_lang_codes.keys():
                        raise ConfigError(f'{lang} is not a valid language')
            elif key == 'gib_langs':
                checktype(value, dict)
                for lang, options in value.items():
                    checktype(lang, str)
                    checktype(options, dict)
                    for opt_name, opt_value in options.items():
                        checktype(opt_value, list)
                        if opt_name == 'pool':
                            if not opt_value:
                                raise ConfigError(f'you must provide at least one language for syllable generation')
                            for lang in opt_value:
                                if lang not in utils.r_lang_codes.keys():
                                    raise ConfigError(f'{lang} is not a valid language')
                        elif opt_name == 'enrich':
                            pass
                        elif opt_name == 'impoverish':
                            pass
                        elif opt_name == 'remove':
                            pass
                        else:
                            raise ConfigError(f'{opt_name} is not a valid option')
            else:
                raise ConfigError(f'{key} is not a valid configuration key')

    def write(self):
        """
        writes the current configuration to file
        """
        self.check()
        utils.general.check_dirs()
        with open(self.user_path, 'w+') as f:
            json.dump(self, f, indent=4)

    def edit(self):
        """
        opens the configuration file in the default text editor
        """
        texteditor.open(filename=self.user_path)

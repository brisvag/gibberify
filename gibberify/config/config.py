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
from pathlib import Path
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
    def __init__(self, *args, path=None, default=False, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        if path is None:
            path = utils.conf
        else:
            path = Path(path)

        # if a dict was passed as argument, don't update based on a config
        if not self:
            if not path.is_file() or default:
                with open(utils.conf_default, 'r') as f:
                    self.update(json.load(f))
            else:
                with open(path, 'r') as f:
                    self.update(json.load(f))

        self.path = path

        self._check()

    def _check(self):
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

        # make sure languages only appear once in real_langs
        unique = set(self['real_langs'])
        self['real_langs'] = list(unique)
        self['real_langs'].sort()

    def write(self):
        """
        writes the current configuration to file
        """
        self._check()
        utils.check_dirs()
        with open(self.path, 'w+') as f:
            json.dump(self, f, indent=4)

    def edit(self):
        """
        opens the configuration file in the default text editor
        """
        texteditor.open(filename=self.path)

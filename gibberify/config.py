# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

"""
Configuration file for gibberify.
You can edit this file manually or through the program customize dictionary generation.
"""

# natural languages used for syllable generation and everything else
# add, remove or comment out lines to edit the base list
__real_langs__ = (
    'en',   # english
    'it',   # italian
    'de',   # german
    'fr',   # french
    'ru',   # russian
    'es',   # spanish
    'nl',   # dutch
    'ca',   # catalan
    'el',   # greek
    'et',   # estonian
    'is',   # icelandic
    'lt',   # lithuanian
    'nb',   # norwegian
    'pt',   # portuguese
    'sk',   # slovak
)

# gibberish languages and their relative settings
# language codes should be 3 letters long, to avoid conflict with real languages
# 'pool' is the list of languages to draw syllables from
# TODO: additional settings will be added here in the future
__gib_langs__ = {
    'orc': {
        'pool': ['ru', 'de'],
        'notimplemented_setting': 'something_awesome'
    },
    'elv': {
        'pool': ['fr', 'en'],
        'notimplemented_setting': 'something_boring'
    },
    'dwa': {
        'pool': ['it', 'de'],
        'notimplemented_setting': 'something_smelly'
    },
}

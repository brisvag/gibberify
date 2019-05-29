"""
This file contains the settings for the other modules
"""


# natural languages used for syllable generation (lang. codes may need locales, eg: en-GB)
langs_download = ('en-GB', 'it', 'de', 'fr', 'ru')

# polished, no-locale version of langs_download
real_langs = tuple(l.split('-')[0] for l in langs_download)

# fake languages and their relative syllable pools
gib_langs = {
    'orc': ['ru', 'de'],
    'elv': ['fr', 'en'],
    'dwa': ['it', 'de'],
}

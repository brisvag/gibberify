"""
Configuration file
"""


# natural languages used for syllable generation (lang. codes may need locales, eg: en-GB)
__real_langs__ = (
                      'en-GB',  # english
                      'it',     # italian
                      'de',     # german
                      'fr',     # french
                      'ru',     # russian
                      'es',     # spanish
                      'nl',     # dutch
                      'ca',     # catalan
                      'el',     # greek
                      'et',     # estonian
                      'is',     # icelandic
                      'lt',     # lithuanian
                      'nb',     # norwegian
                      'pt',     # portuguese
                      'sk',     # slovak
                      )

# fake languages and their relative syllable pools
__gib_langs__ = {
    'orc': ['ru', 'de'],
    'elv': ['fr', 'en'],
    'dwa': ['it', 'de'],
}

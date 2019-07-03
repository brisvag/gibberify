"""
Collection of utilities and globals
"""

import os
import sys


__version__ = 0.1


if hasattr(sys, "_MEIPASS"):
    __data__ = os.path.join(sys._MEIPASS, 'data')
else:
    __data__ = os.path.join(os.path.dirname(__file__), 'data')


def code(lang):
    """
    strips locale info from language

    returns 2-letter code
    """
    return lang.split('-')[0]


def progress(message, partial, total):
    """
    print progress in percentage with carriage return
    """
    # +0.5 is to round up
    print(f'\r{message}: {int((partial/total)*100+0.5)}%', flush=True, end='')
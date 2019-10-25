# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

from .utils import r_lang_codes, syllabize, __version__
from .config import Config
from .generate import Syllabizer, Scrambler, build
from .translate import Translator
from .ui import gui, interactive

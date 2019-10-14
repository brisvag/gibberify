# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

import pytest
from contextlib import suppress
from gibberify import Translator


@pytest.fixture
def tr():
    # need to suppress because load_dicts tries to load files that don't exist. It's fine
    # because we provide a dummy file right after
    with suppress(FileNotFoundError):
        tr = Translator(lang_in='en', lang_out='orc', text_in='test')
    tr.dicts = {
        'en-orc': {'test': 'test_trans', 'word': 'word_trans'},
        'orc-en': {1: {'test_trans': 'test'}}
    }
    return tr


def test_translator_instance(tr):
    assert isinstance(tr, Translator)
    assert Translator.lang_in == 'en'
    assert Translator.lang_out == 'orc'
    assert Translator.text_in == 'test'
    assert isinstance(Translator.dicts, dict)
    assert isinstance(Translator.dict, dict)


def test_run(tr):
    tr.run()
    assert tr.text_out == 'test_trans'


def test_setattr(tr):
    tr.run()
    tr.text_in = 'word'
    assert tr.text_out == 'word_trans'


def test_gibberify(tr):
    tr.gibberify()
    assert tr.text_out == 'test_trans'


def test_reverse(tr):
    tr.lang_in = 'orc'
    tr.lang_out = 'en'
    tr.text_in = 'test_trans'
    tr.degibberify()
    assert tr.text_out == 'test'

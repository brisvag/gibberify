# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

import pytest
from gibberify import Translator
from gibberify.generate.dicts import GibDict


@pytest.fixture
def tr():
    conf = {
        'pool': ['en'],
        'enrich': ['t'],
        'impoverish': [],
        'remove': ['w']
    }
    dicts = {
        'en-orc': GibDict('en', 'orc', conf, {'te': 'stu', 'st': 'ff'}),
        'orc-en': GibDict('orc', 'en', conf, {3: {'stu': 'te'}, 2: {'ff': 'st'}}, reverse=True)
    }
    return Translator(lang_in='en', lang_out='orc', text_in='test', dicts=dicts)


def test_translator_instance(tr):
    assert isinstance(tr, Translator)
    assert tr.lang_in == 'en'
    assert tr.lang_out == 'orc'
    assert tr.text_in == 'test'
    assert isinstance(tr.dicts, dict)


def test_run(tr):
    assert tr.text_out == 'stuff'


def test_setattr(tr):
    tr.text_in = 'te'
    assert tr.text_out == 'stu'


def test_degibberify(tr):
    tr.lang_in = 'orc'
    tr.lang_out = 'en'
    tr.text_in = 'stuff'
    tr.degibberify()
    assert tr.text_out == 'test'

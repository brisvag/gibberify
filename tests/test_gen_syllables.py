# Copyright 2019-2019 the gibberify authorsyl. See copying.md for legal info.

import pytest
from gibberify import Syllabizer
from gibberify.generate.syllables import GibPool
from gibberify.utils import access_data


@pytest.fixture
def syl():
    return Syllabizer(lang='en')


def test_syllabizer_instance(syl):
    assert isinstance(syl, Syllabizer)
    assert syl.lang == 'en'


def test_download_raw(syl):
    raw = syl._download_raw()
    assert isinstance(raw, list)
    assert raw


def test_download_words(syl):
    words = syl._download_words()
    assert isinstance(words, GibPool)
    assert words


def test_download_syllables(syl):
    syllables = syl._download_syllables()
    assert isinstance(syllables, GibPool)
    assert syllables


@pytest.mark.incremental
class TestSyllablizerWriteRead:
    def test_write(self, syl):
        syl.words = GibPool('en', ['another', 'thing'])
        syl.syllables = GibPool('en', ['more', 'stuff'])
        syl._save(words=True, sylables=True)
        words = access_data('words', 'en')
        syllables = access_data('syllables', 'en')
        assert words == syl.words
        assert syllables == syl.syllables

    def test_load_words(self, syl):
        words = syl._load_words()
        assert isinstance(words, GibPool)
        assert words

    def test_load_syllables(self, syl):
        syllables = syl._load_syllables()
        assert isinstance(syllables, GibPool)
        assert syllables


def test_make_words(syl):
    syl.raw = [b'test', b'word']
    words = syl._make_words()
    assert isinstance(words, GibPool)
    assert words


def test_make_syllables(syl):
    syl.words = GibPool('en', ['another', 'thing'])
    syllables = syl._make_syllables()
    assert isinstance(syllables, GibPool)
    assert syllables

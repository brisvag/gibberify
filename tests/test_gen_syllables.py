# Copyright 2019-2019 the gibberify authorsyl. See copying.md for legal info.

import pytest
from gibberify import Syllabizer
from gibberify.utils import access_data


@pytest.fixture
def syl():
    return Syllabizer(lang='en')


def test_syllabizer_instance(syl):
    assert isinstance(syl, Syllabizer)
    assert syl.lang == 'en'


def test_download_raw(syl):
    syl.download_raw()
    assert isinstance(syl.raw, list)
    assert syl.raw


# TODO: first need to implement this in gibberify and upload to gibberify-data
# def test_download_words(syl):
#     syl.download_words()
#     assert isinstance(syl.words, list)
#     assert syl.words.readlines()


def test_download_syllables(syl):
    syl.download_syllables()
    assert isinstance(syl.syllables, list)
    assert syl.syllables


@pytest.mark.incremental
class TestSyllablizerWriteRead:
    def test_write(self, syl):
        syl.raw = ['test', 'word']
        syl.words = ['another', 'thing']
        syl.syllables = ['more', 'stuff']
        syl.write(raw=True, words=True, syllables=True)
        raw = access_data('raw', 'en')
        words = access_data('words', 'en')
        syllables = access_data('syllables', 'en')
        assert raw == syl.raw
        assert words == syl.words
        assert syllables == syl.syllables

    def test_load_words(self, syl):
        syl.load_words()
        assert isinstance(syl.words, list)
        assert syl.words

    def test_load_syllables(self, syl):
        syl.load_syllables()
        assert isinstance(syl.syllables, list)
        assert syl.syllables


def test_make_words(syl):
    syl.raw = [b'test', b'word']
    syl.make_words()
    assert isinstance(syl.words, list)
    assert syl.words


def test_make_syllables(syl):
    syl.words = ['another', 'thing']
    syl.make_syllables()
    assert isinstance(syl.syllables, list)
    assert syl.syllables


# def test_run(syl):
#     syl.run(from_raw=True)
#     syl.run(force_syl_rebuild=True)
#     syl.run()

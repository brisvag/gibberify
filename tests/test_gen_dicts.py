# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

import pytest
from gibberify import Scrambler
from gibberify.utils import access_data


@pytest.fixture
def scr():
    gib_conf_test = {
        'pool': ['en'],
        'enrich': ['t'],
        'impoverish': [],
        'remove': ['w']
    }
    scr = Scrambler(real_lang='en', gib_lang='orc', gib_conf=gib_conf_test)
    return scr


def test_scrambler_instance(scr):
    assert isinstance(scr, Scrambler)
    assert scr.real_lang == 'en'
    assert scr.gib_lang == 'orc'
    assert scr.gib_conf == {
        'pool': ['en'],
        'enrich': ['t'],
        'impoverish': [],
        'remove': ['w']
    }


def test_create_gib_pool(scr):
    scr.gib_pool_raw = ['test', 'word']
    scr._create_gib_pool()
    assert isinstance(scr.gib_pool, list)
    assert 'test' in scr.gib_pool
    assert 'word' not in scr.gib_pool


def test_straight(scr):
    scr.real_pool = ['test', 'word']
    scr.gib_pool = ['another', 'thing']
    scr._make_straight()
    assert isinstance(scr.dict_straight, dict)
    assert scr.dict_straight


def test_reverse(scr):
    scr.dict_straight = {'test': 'word'}
    scr._reverse()
    assert isinstance(scr.dict_reverse, dict)
    # TODO this thing shouldn't be a string sometimes and an int ome other time!
    assert scr.dict_reverse == {4: {'word': 'test'}}


def test_write(scr):
    scr.dict_straight = {'test': 'word'}
    scr.dict_reverse = {'4': {'word': 'test'}}
    scr._save()
    straight = access_data('dicts', 'en', 'orc')
    reverse = access_data('dicts', 'orc', 'en')
    assert scr.dict_straight == straight
    assert scr.dict_reverse == reverse

# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

import pytest
import json
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
    scr.create_gib_pool()
    assert isinstance(scr.gib_pool, list)
    assert 'test' in scr.gib_pool
    assert 'word' not in scr.gib_pool


def test_straight(scr):
    scr.real_pool = ['test', 'word']
    scr.gib_pool = ['another', 'thing']
    scr.straight()
    assert isinstance(scr.dict_straight, dict)
    assert scr.dict_straight


def test_reverse(scr):
    scr.dict_straight = {'test': 'word'}
    scr.reverse()
    assert isinstance(scr.dict_reverse, dict)
    assert scr.dict_reverse == {4: {'word': 'test'}}


def test_write(scr):
    scr.dict_straight = {'test': 'word'}
    scr.dict_reverse = {4: {'word': 'test'}}
    scr.write()
    straight = json.load(access_data('dicts', 'en', 'orc'))
    reverse = json.load(access_data('dicts', 'orc', 'en'))
    assert scr.dict_straight == straight
    assert scr.dict_reverse == reverse

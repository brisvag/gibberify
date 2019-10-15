# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

import json
from gibberify import Config


def test_from_default():
    cfg = Config.from_default()
    assert 'en' in cfg['real_langs']
    assert 'orc' in cfg['gib_langs'].keys()


def test_write():
    dummy = {
        'real_langs': ['en'],
        'gib_langs': {'orc': {
            'pool': ['en'],
            'enrich': ['x'],
            'impoverish': ['y'],
            'remove': ['z']
        }}
    }
    cfg = Config(dummy)
    cfg.write()
    with open(cfg.user_path, 'r') as f:
        conf = json.load(f)
    assert conf == dummy

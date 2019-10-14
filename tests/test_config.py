# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

# import json
# from gibberify import Config
#
#
# def test_from_default():
#     cfg = Config.from_default()
#     assert 'en' in cfg.keys()
#
#
# def test_write():
#     cfg = Config({'test': 'word'})
#     cfg.write()
#     with open(cfg.user_path, 'r') as f:
#         conf = json.load(f)
#     assert conf == {'test': 'word'}

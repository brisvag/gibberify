# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

from pathlib import Path
from gibberify import utils


def test_globals():
    assert isinstance(utils.version, str)
    assert isinstance(utils.basedir, Path)
    assert utils.basedir.is_dir()
    assert isinstance(utils.assets, Path)
    assert utils.assets.is_dir()
    assert isinstance(utils.data, Path)
    assert utils.data.is_dir()
    assert isinstance(utils.conf, Path)
    assert utils.conf.is_file()


def test_syllabize():
    assert utils.syllabize('test') == ['te', 'st']
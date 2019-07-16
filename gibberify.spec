# -*- mode: python -*-

# Copyright 2019-2019 the gibberify authors. See copying.md for legal info.

import os
from PyInstaller.utils.hooks import collect_data_files


block_cipher = None

added_files = []
added_files += collect_data_files('pyphen')
added_files += collect_data_files('certifi')
added_files += collect_data_files('transliterate', include_py_files=True)
added_files += [(os.path.join('gibberify', 'assets'), 'assets')]
added_files += [(os.path.join('gibberify', 'config.json'), '.')]

extra_imports = ['pyphen', 'transliterate', 'PyQt5', 'certifi', 'texteditor']


a = Analysis(['gibberify/__main__.py'],
             # need to add pyqt binaly dlls for windows to find them
             pathex=['gibberify', '/Python36/Lib/site-packages/PyQt5/Qt/bin'],
             binaries=[],
             datas=added_files,
             hiddenimports=extra_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure,
          a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='gibberify',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True)

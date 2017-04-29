# -*- mode: python -*-

import os
import path
import traceback
block_cipher = None
this_dir = os.path.dirname(os.path.realpath('__file__'))
a = Analysis(['main.py'],
             pathex=[this_dir],
             binaries=[],
             datas=[ ("demos", "demos")],
             hiddenimports=["PyQt5.QtCore.*","PyQt5.*" ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PyJeopardy')

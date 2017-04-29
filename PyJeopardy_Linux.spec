# -*- mode: python -*-

import os
import path
import traceback
block_cipher = None

this_dir = os.path.dirname(os.path.realpath('__file__'))
print(this_dir)
vlc_lib_include = []
lib_paths = ['/usr/lib/', '/usr/lib/x86_64-linux-gnu/', '/lib/', '/lib/x86_64-linux-gnu/']
for l in lib_paths:
    if(l + "vlc" in path.path(l).dirs()):
        vlc_lib_path = [ (l + "vlc", "vlc")]
        break

a = Analysis(['main.py'],
             pathex=[this_dir],
             binaries=[],
             datas=[ ("demos", "demos")] + vlc_lib_path,
             hiddenimports=[],
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

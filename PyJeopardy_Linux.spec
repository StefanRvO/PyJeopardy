# -*- mode: python -*-

import os
import path
import traceback
block_cipher = None

this_dir = os.path.dirname(os.path.realpath('__file__'))
print(this_dir)
vlc_lib_include = []
vlc_lib_path = ""
lib_path = ""
lib_paths = ['/usr/lib/', '/usr/lib/x86_64-linux-gnu/', '/lib/', '/lib/x86_64-linux-gnu/']
for l in lib_paths:
    if(l + "vlc" in path.path(l).dirs()):
        for f in path.path(l).files(pattern="libvlc.so"):
            print(f)
            vlc_lib_include.append( (f,  "") )
        for f in path.path(l).files(pattern="libvlccore.so"):
            print(f)
            vlc_lib_include.append( (f,  "") )
        vlc_lib_path = [ (l + "vlc", "")]
        break

print(vlc_lib_include)
a = Analysis(['main.py'],
             pathex=[this_dir],
             binaries=vlc_lib_include,
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

#Single file
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='PyJeopardy',
          debug=False,
          strip=False,
          upx=True,
          console=True )

#Single folder
"""
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=False,
          upx=True,
          console=True )"""

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PyJeopardy')

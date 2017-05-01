# -*- mode: python -*-

import os
import path
import traceback
block_cipher = None
this_dir = os.path.dirname(os.path.realpath('__file__'))
vlc_path = this_dir + os.sep + "vlc" + os.sep

qt_lib_path = "C:" + os.sep + "Python35" + os.sep + "Lib" + os.sep + "site-packages" + os.sep + "PyQt5" + os.sep + "Qt" + os.sep + "bin"
print(qt_lib_path)

print(this_dir)
a = Analysis(['main.py'],
             pathex=[this_dir, qt_lib_path],
             binaries=[(vlc_path + "libvlc.dll", ""), 
			(vlc_path + "libvlccore.dll", "")],
             datas=[ ("demos", "demos"),
			("plugins", "plugins")],
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
          name='PyJeopardy',
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

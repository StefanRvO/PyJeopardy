#This builds an executable using cx_freeze
import sys
from cx_Freeze import setup, Executable
import os
import path
# Dependencies are automatically detected, but it might need fine tuning.
bin_includes = []
if sys.platform == "win32":
    pass
else:
    lib_path = path.path('/usr/lib/')
    for f in lib_path.files(pattern='libssl.so.*'):
        bin_includes.append(f)

    for f in lib_path.files(pattern='libcrypto.so.*'):
        bin_includes.append(f)
    for f in lib_path.files(pattern='libvlc.so.*'):
        bin_includes.append(f)
    for f in lib_path.files(pattern='libvlccore.so.*'):
        bin_includes.append(f)

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = { 'include_msvcr': True, "packages": ["codecs", "vlc", "urllib", "ssl", "os",], \
    "include_files" : ['demos/'],
    'bin_includes' : bin_includes}
# GUI applications require a different base on Windows (the default is for a
# console application).
bdist_msi_options = { }
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "PyJeopardy",
        version = "0.1",
        description = "PyJeopardy!",
        options = {"build_exe": build_exe_options, "bdist_msi": bdist_msi_options},
        executables = [Executable("main.py", base=base)])

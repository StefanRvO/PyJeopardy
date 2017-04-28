#This builds an executable using cx_freeze
import sys
import os
import path
from cx_Freeze import setup, Executable
import requests.certs 
from path import path
lib_path = path('/usr/lib/')
# Dependencies are automatically detected, but it might need fine tuning.
bin_includes = []

for f in lib_path.files(pattern='libssl.so.*'):
    bin_includes.append(f)

for f in lib_path.files(pattern='libcrypto.so.*'):
    bin_includes.append(f)


build_exe_options = { 'include_msvcr': True, "packages": ["codecs", "vlc", "urllib", "ssl", "os", "urllib.request",],
			'include_files' : [ "demos/",],
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
        executables = [Executable("urllib_test.py", base=base)])


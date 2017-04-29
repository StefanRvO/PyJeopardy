#This builds an executable using cx_freeze
import sys
from cx_Freeze import setup, Executable
import os
import path


def add_files_below(add_list, dir_):
    for subdir in path.path(dir_).dirs():
        add_files_below(add_list, subdir)
    for f in path.path(dir_).files():
        bin_includes.append(f)
# Dependencies are automatically detected, but it might need fine tuning.
libs = []
lib_paths = ['/usr/lib/', '/usr/lib/x86_64-linux-gnu/', '/lib', '/lib/x86_64-linux-gnu/']
for l in lib_paths:
    add_files_below(libs, l)

        #add_files_below(bin_includes, vlc_path)
print(bin_includes)
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = { 'include_msvcr': True, "packages": ["codecs", "vlc", "urllib", "ssl", "os",], \
    "include_files" : ['demos/'],
    'bin_includes' : bin_includes,
    'bin_path_includes': lib_paths,}
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

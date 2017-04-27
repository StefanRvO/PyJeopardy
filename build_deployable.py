#This builds an executable using cx_freeze
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = { 'include_msvcr': True, "packages": ["codecs"], }

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

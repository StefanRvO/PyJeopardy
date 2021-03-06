#This builds an executable using cx_freeze
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"compressed":True}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "PyJeopardy",
        version = "0.1",
        description = "PyJeopardy!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])

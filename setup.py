import sys, os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"], "include_files": ['savedServers/']}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"


setup(  name = "client",
    version = "1.0",
    description = "My application!",
    options = {"build_exe": build_exe_options},
    executables = [Executable("client.py", base = base)])

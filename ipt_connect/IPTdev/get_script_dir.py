#!/usr/bin/env python
import inspect
import os
import sys


# https://stackoverflow.com/questions/3718657/how-to-properly-determine-current-script-directory/22881871#22881871
def get_script_dir(follow_symlinks=True):
    if getattr(sys, "frozen", False):  # py2exe, PyInstaller, cx_Freeze
        path = os.path.abspath(sys.executable)
    else:
        path = inspect.getabsfile(get_script_dir)
    if follow_symlinks:
        path = os.path.realpath(path)
    return os.path.dirname(path)

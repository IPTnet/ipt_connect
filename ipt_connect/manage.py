#!/usr/bin/env python
import os
import sys


def is_po_updated(path):
    for root, _, files in os.walk(path):
        if len(files) == 1:
            return 1
        try:
            po = os.path.getmtime(root + "/" + files[0])
            mo = os.path.getmtime(root + "/" + files[1])
        except IndexError:
            continue
        if po > mo:
            return 1
    return 0


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ipt_connect.settings")

    from django.core.management import execute_from_command_line

    if sys.argv[1] == "runserver":
        if is_po_updated("locale") or is_po_updated("loginas/locale"):
            execute_from_command_line(["manage.py", "compilemessages"])

    execute_from_command_line(sys.argv)

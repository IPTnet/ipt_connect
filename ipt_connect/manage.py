#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ipt_connect.settings")

    from django.core.management import execute_from_command_line

    if sys.argv[1] == 'runserver':
        mo = os.path.getmtime('locale/ru/LC_MESSAGES/django.mo')
        po = os.path.getmtime('locale/ru/LC_MESSAGES/django.po')
        if po > mo:
            execute_from_command_line(['manage.py', 'compilemessages'])

    execute_from_command_line(sys.argv)

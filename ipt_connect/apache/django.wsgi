#!/usr/bin/python

import os, sys
#sys.path.append (os.path.expanduser ('~kim'))
#sys.path.append (os.path.expanduser ('~kim/kim'))
sys.path = ["/var/www/kim/kim/"] + sys.path
sys.path = ["/var/www/kim/kim/ipt_connect"] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

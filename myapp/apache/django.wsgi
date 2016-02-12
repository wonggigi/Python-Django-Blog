import os

import sys

path = '/media/新加卷/hanio/project/myapp'

if path not in sys.path:

    sys.path.insert(0, '/media/新加卷/hanio/project/myapp')

os.environ['DJANGO_SETTINGS_MODULE'] = 'myapp.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

import os
import sys

path='/var/www/part4_project'

if path not in sys.path:
  sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'part4_project.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
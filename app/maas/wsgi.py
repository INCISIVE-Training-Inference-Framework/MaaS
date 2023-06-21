import os

from static_ranges import Ranges
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maas.settings')

application = Ranges(get_wsgi_application())

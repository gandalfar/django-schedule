from django.core.management import setup_environ
from future_todo import settings
setup_environ(settings)
from t3p.views import plugin_handler
#from django.conf import settings

settings.plugin_handler = plugin_handler

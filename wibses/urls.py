from django.conf.urls import patterns, url
from wibses.views import script

urlpatterns = patterns('',
    url(r'^data/script$', script, name='script_crud'),
)

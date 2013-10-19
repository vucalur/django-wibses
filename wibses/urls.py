from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from wibses.views import script

urlpatterns = patterns('',
    url(r'^data/script$', script, name='script_crud'),
)

urlpatterns += staticfiles_urlpatterns()
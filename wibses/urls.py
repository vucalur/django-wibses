from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from wibses.views import script
from wibses.views import token


urlpatterns = patterns('',
    url(r'^data/script$', script, name='script_crud'),
    url(r'^dicapi/(?P<token_form>.*)$', token)
)

urlpatterns += staticfiles_urlpatterns()
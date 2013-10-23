from django.conf.urls import patterns, url
from wibses.views import script
from wibses.views import token

urlpatterns = patterns('',
    url(r'^data/script$', script, name='script_crud'),
    url(r'^dicapi/(?P<token_form>.*)$', token)
)

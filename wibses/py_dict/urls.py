from django.conf.urls import patterns, url
from wibses.py_dict.views import rest__get_tokens

urlpatterns = patterns('',
    url(r'^token/(?P<token_form>.*)$', rest__get_tokens, name='script_crud'),
)
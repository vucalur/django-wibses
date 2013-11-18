from django.conf.urls import patterns, url

from wibses.data_store.views import rest__list_storage_scripts, rest__save_script_in_storage, \
    rest__list_script_history, rest__get_script_of_revision, rest__fork_script_of_revision, \
    rest__create_new_script, rest__get_script, rest__params_api


urlpatterns = patterns('',
    url(r'^scripts$', rest__list_storage_scripts),
    url(r'^scripts/(?P<script_name>\w([\w_\d\.])*)$', rest__get_script),
    url(r'^scripts/save/(?P<script_name>\w([\w_\d\.])*)$', rest__save_script_in_storage),
    url(r'^scripts/hist/(?P<script_name>\w([\w_\d\.])*)$', rest__list_script_history),
    url(r'^scripts/hist/(?P<script_name>\w([\w_\d\.])*)/(?P<revision>[0-9a-z]+)$', rest__get_script_of_revision),
    url(r'^scripts/hist/fork/(?P<script_name>\w([\w_\d\.])*)/(?P<revision>[0-9a-z]+)$', rest__fork_script_of_revision),
    url(r'^scripts/create/(?P<script_name>\w([\w_\d\.])*)$', rest__create_new_script),
    url(r'^api$', rest__params_api)
)

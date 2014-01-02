from django.conf.urls import patterns, url

import views


urlpatterns = patterns('',
    url(r'^scripts$', views.rest__list_storage_scripts),
    url(r'^scripts/(?P<script_id>\w([\w_\d\.])*)$', views.rest__get_script),
    url(r'^scripts/save/(?P<script_id>\w([\w_\d\.])*)$', views.rest__save_script_in_storage),
    url(r'^scripts/hist/(?P<script_id>\w([\w_\d\.])*)$', views.rest__list_script_history),
    url(r'^scripts/hist/(?P<script_id>\w([\w_\d\.])*)/(?P<revision>[0-9a-z]+)$', views.rest__get_script_of_revision),
    url(r'^scripts/hist/fork/(?P<script_id>\w([\w_\d\.])*)/(?P<revision>[0-9a-z]+)$', views.rest__fork_script_of_revision),
    url(r'^create$', views.rest__create_new_script),
    url(r'^get_default$', views.rest__get_default_script),
    url(r'^api$', views.rest__params_api)
)

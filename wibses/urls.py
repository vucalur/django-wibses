from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    url(r'^data/', include('wibses.data_store.urls')),
    url(r'^pydict/', include('wibses.py_dict.urls')),
)

urlpatterns += staticfiles_urlpatterns()
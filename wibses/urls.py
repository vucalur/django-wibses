from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView


urlpatterns = patterns('',
    url(r'^data/', include('wibses.data_store.urls')),
    url(r'^pydict/', include('wibses.py_dict.urls')),
    url(r'^$', RedirectView.as_view(url="index.html")),
    url(r'^(?P<path>.*)$', 'django.contrib.staticfiles.views.serve'),
)

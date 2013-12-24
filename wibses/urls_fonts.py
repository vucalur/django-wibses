from django.conf.urls import patterns, url
from django.contrib import staticfiles


urlpatterns = patterns('',
    url(r'^(?P<font_file>.*)$', lambda request, font_file: staticfiles.views.serve(request, 'fonts/' + font_file)),
)

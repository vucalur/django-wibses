from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^wibses/', include('django-wibses.wibses.urls', namespace='wibses')),
)

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', include('base.urls'), name='base'),
    url(r'^on-boarding/', include('base.urls'), name='on_boarding'),
    url(r'^auction/', include('auction.urls'), name='auction'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

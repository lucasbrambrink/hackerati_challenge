from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^auction/', include('auction.urls'), name='auction'),
    url(r'^admin/', include(admin.site.urls)),
)

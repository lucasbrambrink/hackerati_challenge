from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from base.views import OnBoardingTemplate

urlpatterns = patterns('',
    url(r'^$', OnBoardingTemplate.as_view(), name='on_boarding'),
    url(r'^auction/', include('auction.urls'), name='auction'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

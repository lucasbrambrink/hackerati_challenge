from django.conf.urls import patterns, include, url
from .views import OnBoardingView, OnBoardingAPI

urlpatterns = patterns('',
    url(r'^$', OnBoardingView.as_view(), name='auction'),
    url(r'^user/(?P<action>[a-z]+)/$', OnBoardingAPI.as_view(), name='api')
)

from django.conf.urls import patterns, include, url
from .views import OnBoardingView

urlpatterns = patterns('',
    url(r'^$', OnBoardingView.as_view(), name='auction'),
    url(r'^create/new/user/$', OnBoardingView.as_view(), name='create')
)

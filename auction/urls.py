from django.conf.urls import patterns, include, url
from .views import AuctionView

urlpatterns = patterns('',
    url(r'^$', AuctionView.as_view(), name='auction'),
)

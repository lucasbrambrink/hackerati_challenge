from django.conf.urls import patterns, include, url
from .views import AuctionView

urlpatterns = patterns('',
    url(r'^$', AuctionView.as_view(), name='auction'),
    url(r'^new/bid/', AuctionView.as_view(), name='create_bid')
)

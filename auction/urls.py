from django.conf.urls import patterns, include, url
from .views import AuctionTemplateView, BiddingView, AuctionView

urlpatterns = patterns('',
    url(r'^$', AuctionTemplateView.as_view(), name='auction'),
    url(r'^bid/(?P<action>[a-z]+)/', BiddingView.as_view(), name='bid-rest'),
    url(r'^auction/(?P<action>[a-z]+)/', AuctionView.as_view(), name='auction-rest')
)

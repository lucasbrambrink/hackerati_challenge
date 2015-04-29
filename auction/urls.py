from django.conf.urls import patterns, include, url
from .views import AuctionTemplateView, BiddingView, AuctionView, ItemView

urlpatterns = patterns('',
    url(r'^$', AuctionTemplateView.as_view(), name='auction'),
    url(r'^bid/(?P<action>[a-z]+)/', BiddingView.as_view(), name='bid-rest'),
    url(r'^item/(?P<action>[a-z]+)/', ItemView.as_view(), name='item-rest'),
    url(r'^auction/(?P<action>[a-z]+)/', AuctionView.as_view(), name='auction-rest')
)

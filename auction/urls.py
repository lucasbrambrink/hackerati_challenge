from django.conf.urls import patterns, include, url
from .views import AuctionTemplateView, BiddingView, AuctionView

urlpatterns = patterns('',
    url(r'^$', AuctionTemplateView.as_view(), name='auction'),
    url(r'^bid/(?<action>[\w-]+)/', BiddingView.as_view(), name='bid-rest'),
    url(r'^auction/(?<action>[\w-]+)/', AuctionView.as_view(), name='auction-rest')
)

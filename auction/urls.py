from django.conf.urls import patterns, include, url
from views import AuctionView

urlpatterns = patterns('',
    url(r'^$', AuctionView.as_view(), name='auction'),
    # url(r'^$', 'auction_hackerati.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
)

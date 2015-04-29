from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import InventoryItem, Auction, Bid
from base.models import HackeratiUser
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
import json

# Create your views here.

class AuctionView(TemplateView):
    template_name = 'auction/main.html'

    def get(self, request, *args, **kwargs):
        user_id = request.session.get('id')
        if user_id:
            user = HackeratiUser.objects.get(id=int(user_id))

        # cannot filter by properties
        active_auction = [auction for auction in Auction.objects.all() if auction.is_active]

        return render(request, self.template_name, {
            'user': user,
            'auctions': active_auction,
        })

    def post(self, request, *args, **kwargs):
        user_id = request.session.get('id')
        if user_id:
            user = HackeratiUser.objects.get(id=int(user_id))

        post = json.loads(request.POST['data'])
        auction_id = post['id']
        amount = post['amount']

        new_bid = Bid(
            user_id=user_id,
            auction_id=auction_id,
            price=amount
        )
        new_bid.save()

        return JsonResponse({
            'username': user.username,
            'price': "${0:.2f}".format(float(amount)),
            'time': new_bid.created_at,
        })


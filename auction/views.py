from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import InventoryItem, Auction
from base.models import HackeratiUser

# Create your views here.

class AuctionView(TemplateView):
    template_name = 'auction/main.html'

    def get(self, request, *args, **kwargs):
        user_id = request.session.get('id')
        if user_id:
            user = HackeratiUser.objects.get(id=int(user_id))

        return render(request, self.template_name, {
            'user': user,
            'items': InventoryItem.objects.all(),
            'auctions': Auction.objects.all(),
        })


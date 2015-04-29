from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from .models import InventoryItem, Auction, Bid
from .scripts import AuctionInitiator
from base.models import HackeratiUser
from django.http import JsonResponse
import json


# Create your views here.

class AuctionTemplateView(TemplateView):
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


###---< Bid CRUD >---###
class BiddingView(View):

    def post(self, request, action='create', *args, **kwargs):
        if action == 'create':
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


###---< Auction Logic >---###
class AuctionView(View):

    def post(self, request, action='create', *args, **kwargs):
        user_id = request.session.get('id')
        if user_id:
            user = HackeratiUser.objects.get(id=int(user_id))
        post = json.loads(request.POST['data'])


        if action == 'create':
            auction_initiator = AuctionInitiator(user_id=user.id)

            create_type = post['type']
            duration = post['duration'] if 'duration' in post else 3

            if create_type == 'all':
                success = auction_initiator.initiate_auction_from_all_items()

            elif create_type == 'specific':
                item_id = post['item_id']
                item = InventoryItem.objects.get(id=int(item_id))
                new_auction = Auction(
                    user_id=user.id,
                    hours_duration=duration,
                    item=item,
                )
                new_auction.save()
                success = True

            return JsonResponse({
                'success': success
            })

        elif action == 'update':
            pass

        elif action == 'ending':
            auction_id = post['id']
            auction = Auction.objects.get(id=int(auction_id))


            auction.on_finish()
            auction.save()

            receiver = None
            if auction.was_successful:
                receiver = auction.item.purchase.first().user

            return JsonResponse({
                'success': auction.was_successful,
                'receiver': receiver,
            })

        elif action == 'delete':
            pass

        elif action == 'import':
            auction_initiator = AuctionInitiator(user_id=user.id)
            import_type = post['import_type']

            if import_type == 'query':
                query = post['query']
                query = query if len(query) else 'furniture'
                success = auction_initiator.perform_sync_from_craigslist(query, 10)

            if import_type == 'random':
                success = auction_initiator.perform_random_sync_from_craigslist(10)

            return JsonResponse({
                'success': success
            })














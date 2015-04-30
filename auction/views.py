from django.conf import settings
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.template import RequestContext
from .models import InventoryItem, Auction, Bid
from .import_scripts import ImportHandler, sync_new_items_from_csv
from base.models import HackeratiUser
from base.utils import FormatHelper as fh
from django.http import JsonResponse
import json

if not settings.DEBUG:
    # Redis & Worker
    from rq import Queue
    from auction_hackerati.worker import conn
    q = Queue(connection=conn)


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
        }, RequestContext(request))


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

            auction = Auction.objects.get(id=int(auction_id))

            user.subtract_from_balance(auction, amount)

            new_bid = Bid(
                user_id=user_id,
                auction_id=auction_id,
                price=amount
            )

            new_bid.save()
            return JsonResponse({
                'username': user.username,
                'price': fh.format_money(amount),
                'time': new_bid.created_at,
                'balance': fh.format_money(user.balance),
            })


###---< Auction Logic >---###
class AuctionView(View):

    def get(self, request, action='data', *args, **kwargs):
        auction_data = Auction.graphing_data()
        inventory_data = InventoryItem.graphing_data()

        return JsonResponse({
            'auction_data': auction_data,
            'inventory_data': inventory_data
        })


    def post(self, request, action='create', *args, **kwargs):
        user_id = request.session.get('id')
        if user_id:
            user = HackeratiUser.objects.get(id=int(user_id))
        post = json.loads(request.POST['data'])


        if action == 'create':
            auction_initiator = ImportHandler(user_id=user.id)

            create_type = post['type']
            duration = post['duration'] if 'duration' in post else 3

            if create_type == 'all':
                success = auction_initiator.initiate_auction_from_all_items(duration=duration)

            return JsonResponse({
                'success': success
            })

        elif action == 'update':
            pass

        elif action == 'ending':
            auction_id = post['auction_id']
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



###---< Uses Redis Queue to Handle Worker >---###
class ItemView(View):

    def delete(self, user, post):
        item_id = post['item_id']
        item = InventoryItem.objects.get(id=int(item_id))
        for auction in item.auction.all():
            auction.delete()
        item.delete()
        return True

    def initialize_new_auction(self, user, post):
        item_id = post['item_id']
        duration = post['duration']
        if not len(duration):
            duration = 1
        item = InventoryItem.objects.get(id=int(item_id))
        if not item.is_being_auctioned:
            new_auction = Auction(
                hours_duration=duration,
                item_id=int(item_id),
                user=user
            )
            new_auction.save()
        return True

    def import_new_items(self, user, post):
        query = post['query']
        if not len(query):
            query = 'furniture'

        if not settings.DEBUG:
            q = Queue(connection=conn)
            q.enqueue(sync_new_items_from_csv, user.id)
            success = True

        else:
            success = ImportHandler.import_items_from_csv(number_of_items=10)

        return JsonResponse({
            'success': success
        })

    def post(self, request, action=None, *args, **kwargs):
        user_id = request.session.get('id')
        if user_id:
            user = HackeratiUser.objects.get(id=int(user_id))
        post = json.loads(request.POST['data'])
        success = False

        if action == 'delete':
            item_id = post['item_id']
            item = InventoryItem.objects.get(id=int(item_id))
            for auction in item.auction.all():
                auction.delete()
            item.delete()
            success = True

        elif action == 'init':
            item_id = post['item_id']
            duration = post['duration']
            if not len(duration):
                duration = 1
            item = InventoryItem.objects.get(id=int(item_id))
            if not item.is_being_auctioned:
                new_auction = Auction(
                    hours_duration=duration,
                    item_id=int(item_id),
                    user=user
                )
                new_auction.save()

        elif action == 'import':
            auction_initiator = ImportHandler(user_id=user.id)
            import_type = post['import_type']
            query = post['query']
            query = query if len(query) else 'furniture'
            if not settings.DEBUG:
                q = Queue(connection=conn)
                q.enqueue(sync_new_items_from_csv, user.id)
                success = True
            else:
                success = auction_initiator.perform_sync_from_craigslist(query, 10)

            return JsonResponse({
                'success': success
            })


        return JsonResponse({
                'success': success
        })









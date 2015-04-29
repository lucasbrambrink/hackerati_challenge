from .models import InventoryItem, Auction
import random

class AuctionInitiator(object):

    def __init__(self):
        pass

    def initiate_auction_from_all_items(self):
        for item in InventoryItem.objects.all():
            if not item.is_sold:
                new_auction = Auction(
                    hours_duration=random.randint(12, 24),
                    item=item,
                )
                new_auction.save()
        return True
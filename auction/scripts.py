from .models import InventoryItem, Auction

class AuctionInitiator(object):

    def __init__(self):
        pass

    def initiate_auction_from_all_items(self):
        for item in InventoryItem.objects.all():
            if not item.is_sold:
                new_auction = Auction(
                    hours_duration=48,
                    item=item,
                )
                new_auction.save()
        return True
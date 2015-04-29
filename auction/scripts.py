from .models import InventoryItem, Auction
from .import_scripts import AutoPopulateThroughCraigslist
import random
from time import sleep

class AuctionInitiator(object):

    def __init__(self, user_id=1):
        self.user_id = user_id


    def master_init_all_items(self):
        for item in InventoryItem.objects.all():
            if not item.is_being_auctioned:
                sleep(random.randint(15, 75))
                if not item.is_sold:
                    new_auction = Auction(
                        user_id=self.user,
                        hours_duration=random.randint(12, 24),
                        item=item,
                    )
                    new_auction.save()

    def initiate_auction_from_all_items(self, duration=1):
        try:
            for item in InventoryItem.objects.filter(user_id=self.user_id):
                if not item.is_being_auctioned:
                    if not item.is_sold:
                        new_auction = Auction(
                            user_id=self.user_id,
                            hours_duration=duration,
                            item=item,
                        )
                        new_auction.save()
            return True
        except:
            return False

    def perform_sync_from_craigslist(self, query=None, max_new=10):
        cl_sync = AutoPopulateThroughCraigslist(self.user_id, number_to_import=max_new)
        try:
            cl_sync.run_global_import(query=query)
            return True
        except:
            return False
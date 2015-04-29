from django.db import models
from django.contrib.auth.models import User
import decimal
# Create your models here.

class HackeratiUser(User):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(decimal_places=2, max_digits=9, default=1000.00)
    is_seller = models.BooleanField(default=False)
    # everyone is a buyer

    def subtract_from_balance(self, auction, amount):
        # if we already have bid on this particular auction-item, only subtract the difference
        self_made_bids = [bid.price for bid in auction.bids.filter(user_id=self.id)]
        if len(self_made_bids):
            highest_bid = max(self_made_bids)
        else:
            highest_bid = 0
        amount = decimal.Decimal(amount) - decimal.Decimal(highest_bid)

        self.balance -= amount
        self.save()

    def add_to_balance(self, amount):
        self.balance += decimal.Decimal(amount)
        self.save()


class Auctioneer(HackeratiUser):
    """
    Inherits from HackeratiUser
    """

    def create_new_auction(self):
        pass

    @property
    def previously_hosted_auctions(self):
        return self.auctions.all()
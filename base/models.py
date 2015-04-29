from django.db import models
from django.contrib.auth.models import User
import decimal
# Create your models here.

class HackeratiUser(User):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(decimal_places=2, max_digits=9, default=1000.00)
    is_seller = models.BooleanField(default=False)
    # everyone is a buyer

    def subtract_from_balance(self, auction_id, amount):
        # if we already have bid on this particular auction-item, only subtract the difference
        highest_bid = max(bid.price for bid in self.bids.filter(auction_id=auction_id))
        if not highest_bid:
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
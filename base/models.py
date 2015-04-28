from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class HackeratiUser(User):
    name = models.CharField(max_length=50)
    balance = models.DecimalField(decimal_places=2, max_digits=9, default=10000.00)
    is_seller = models.BooleanField(default=False)
    # everyone is a buyer


class Auctioneer(HackeratiUser):
    """
    Inherits from HackeratiUser
    """

    def create_new_auction(self):
        pass

    @property
    def previously_hosted_auctions(self):
        return self.auctions.all()
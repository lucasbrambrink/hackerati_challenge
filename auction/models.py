from django.db import models
from django.db.models import ImageField
from base.utils import FormatHelper as fh
from base.models import HackeratiUser
from PIL import Image
from django.conf import settings
from io import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import requests
import datetime
import os


class InventoryItem(models.Model):
    MAX_IMAGE_SIZE = 500

    image = models.ImageField(null=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    reserved_price = models.DecimalField(decimal_places=2, max_digits=9)

    @property
    def is_sold(self):
        return len(self.item.all()) > 0



    ###---< Image Utility Methods >---###
    def upload_image_from_url(self, url):
        """
        :param url: ``str``
        :return: None, mutates self by saving new image
        """
        image_stream = self.fetch_image_stream_from_url(url)

        file_name = fh.pythonify("{name}_{id}.jpg".format(
            name=self.name, price=self.reserved_price, id=self.pk
        ))
        self.remove_same_name(name=file_name)
        django_file = InMemoryUploadedFile(image_stream, None, file_name, 'image/jpeg',
                                  image_stream.len, None)
        # save
        self.image.save(file_name, django_file, save=True)
        self.save()

    def fetch_image_stream_from_url(self, url):
        """
        :param url: ``str``
        :return: ``StringIO`` instance containing the image
        """
        # fetch image from url
        image_stream = requests.get(url)
        image = Image.open(StringIO(image_stream.content))

        # resize image
        original_size = image.size
        limit = max(original_size)
        resize_factor = float(limit) / float(self.MAX_IMAGE_SIZE)
        compressed_size = (int(round(original_size[0] / resize_factor)),
                           int(round(original_size[1] / resize_factor)))
        resized_image = image.resize(compressed_size, Image.ANTIALIAS)

        # upload to stream
        image_stream = StringIO()
        resized_image.save(image_stream, format="JPEG")

        return image_stream

    @staticmethod
    def remove_same_name(name):
        """
        :param name: ``str`` of filename
        :return: None, removes existing file from directory
        """
        for file in os.listdir(settings.MEDIA_ROOT):
            if file == name:
                path = os.path.join(settings.MEDIA_ROOT, file)
                os.remove(path)




class Auction(models.Model):

    bid_log = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hours_duration = models.IntegerField()

    # Item
    item = models.ForeignKey('InventoryItem', related_name='item')
    sold_item = models.BooleanField(default=False)

    # Prices
    current_price = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    starting_price = models.DecimalField(max_digits=9, decimal_places=2)
    end_price = models.DecimalField(max_digits=9, decimal_places=2, null=True)

    ###---< Properties >---###
    @property
    def current_highest_bid(self):
        return max(getattr(bid.price) for bid in self.bids.all())

    @property
    def _starting_price(self):
        return 0.1 * self.item.reserved_price

    @property
    def _end_price(self):
        if self.is_active:
            return False
        return self.current_highest_bid

    @property
    def was_successful(self):
        if self.is_active:
            return False

        return self.end_price >= self.item.reserved_price

    @property
    def ending_datetime(self):
        return self.created_at + datetime.timedelta(hours=self.hours_duration)

    @property
    def is_active(self):
        return self.ending_datetime < datetime.datetime.now(datetime.tzinfo)

    ###---< Internal Methods >---###
    def increase_current_bidding_price(self, value=None):
        if value <= self.current_price:
            return False

        self.current_price = value
        self.save()
        return True

    def request_time(self):
        """ If request time was within ending moments of the auction,
        One would want to extend accepting bids (from the auctioneer's
        perspective, as bids can only increase
        :return:
        """
        pass

    def on_closing(self):

        if not self.was_successful:
            return False

        highest_bid = self.bids.order_by('-price')[0]
        Purchase.objects.create(highest_bid.__dict__)



class Bid(models.Model):

    price = models.DecimalField(decimal_places=2, max_digits=11)
    created_at = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey('Auction', related_name='bids')
    user = models.ForeignKey('base.HackeratiUser', related_name='bids')


class Purchase(models.Model):

    auction = models.ForeignKey('Auction', related_name='purchase')
    item = models.ForeignKey('InventoryItem', related_name='purchase')
    user = models.ForeignKey('base.HackeratiUser', related_name='purchases')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(decimal_places=2, max_digits=9)

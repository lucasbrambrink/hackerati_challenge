from django.db import models
from django.db.models import ImageField
from base.utils import FormatHelper as fh
from base.models import HackeratiUser
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from PIL import Image
from django.conf import settings
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import requests
import datetime
import os


class InventoryItem(models.Model):
    FURNITURE = 'furniture'
    ELECTRONICS = 'electronics'
    JEWELERY = 'jewelery'
    INSTRUMENTS = 'music_instruments'
    TICKETS = 'tickets'
    CATEGORY_CHOICES = (
        (FURNITURE, 'Furniture'),
        (ELECTRONICS, 'Electronics'),
        (JEWELERY, 'Jewelery'),
        (INSTRUMENTS, 'Instruments'),
        (TICKETS, 'Tickets'),
    )
    MAX_IMAGE_SIZE = 300

    image = models.ImageField(null=True)
    image_url = models.CharField(max_length=600, null=False, default='')
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    reserved_price = models.DecimalField(decimal_places=2, max_digits=9)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default=FURNITURE)
    user = models.ForeignKey('base.HackeratiUser', related_name='item')

    @property
    def shortened_name(self):
        return " ".join(word for index, word in enumerate(self.name.split()) if index < 4)

    @property
    def is_being_auctioned(self):
        return len(self.auction.all()) > 0

    @property
    def is_sold(self):
        return len(self.purchase.all()) > 0


    ###---< Image Utility Methods >---###
    def upload_image_from_url(self, url=None):
        """
        :param url: ``str``
        :return: ``bool`` if save successful, (image was large enough)
        """
        url = self.image_url if not url else url

        # fetch image from url
        image = self.fetch_PIL_object_from_url(url)
        # clean and validate size
        cleaned_image = self.clean_image(image)

        # if valid, upload to stream
        image_stream = BytesIO()
        cleaned_image.save(image_stream, format="JPEG")

        # load into django
        file_name = fh.pythonify("{name}_{id}.jpg".format(
            name=self.name, price=self.reserved_price, id=self.pk
        ))
        self.remove_same_name(name=file_name)
        django_file = InMemoryUploadedFile(image_stream, None, file_name, 'image/jpeg', None, None)

        # save
        self.image.save(file_name, django_file, save=True)
        self.save()
        return True


    def clean_image(self, image):
        """
        :param image: ``PIL instance``
        :return: ``PIL instance`` resized
        """
        original_size = image.size
        limit = max(original_size)
        resize_factor = float(limit) / float(self.MAX_IMAGE_SIZE)
        compressed_size = (int(round(original_size[0] / resize_factor)),
                           int(round(original_size[1] / resize_factor)))
        return image.resize(compressed_size, Image.ANTIALIAS)


    def fetch_PIL_object_from_url(self, url):
        """
        :param url: ``str``
        :return: ``PIL instance``
        """
        # fetch image from url
        image_stream = requests.get(url)
        # print (StringIO(image_stream.content))
        return Image.open(BytesIO(image_stream.content))


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



@receiver(post_delete, sender=InventoryItem)
def auto_delete_file_on_delete(sender, instance, *args, **kwargs):
    """auto-delete image jps from filesystem
    upon deleting the `InventoryItem` instance"""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)




class Auction(models.Model):

    user = models.ForeignKey('base.HackeratiUser', related_name='auction')
    bid_log = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hours_duration = models.IntegerField()

    # Item
    item = models.ForeignKey('InventoryItem', related_name='auction')
    sold_item = models.BooleanField(default=False)

    # Prices
    current_price = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    starting_price = models.DecimalField(max_digits=9, decimal_places=2)
    end_price = models.DecimalField(max_digits=9, decimal_places=2, null=True)


    ###---< Properties >---###
    @property
    def current_highest_bid(self):
        if self.bids.count() == 0:
            return 0.0
        return max(getattr(bid, 'price') for bid in self.bids.all())

    @property
    def _starting_price(self):
        return 0.1 * float(self.item.reserved_price)

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
    def seconds_until_expire(self):
        return round((self.ending_datetime - datetime.datetime.now(datetime.timezone.utc)).total_seconds())

    @property
    def is_active(self):
        return self.ending_datetime > datetime.datetime.now(datetime.timezone.utc)

    @property
    def number_of_seconds_left(self):
        delta = self.ending_datetime - datetime.datetime.now(datetime.timezone.utc)
        return delta.total_seconds()

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


@receiver(pre_save, sender=Auction)
def execute_pre_save(sender, instance, *args, **kwargs):
    if not instance.id:
        instance.starting_price = instance._starting_price
    instance.current_price = instance.current_highest_bid.price if instance.bids.count() > 0 else 0




class Bid(models.Model):

    price = models.DecimalField(decimal_places=2, max_digits=11)
    created_at = models.DateTimeField(auto_now_add=True)
    auction = models.ForeignKey('Auction', related_name='bids')
    user = models.ForeignKey('base.HackeratiUser', related_name='bids')

    class Meta:
        ordering = ['-created_at']


class Purchase(models.Model):

    auction = models.ForeignKey('Auction', related_name='purchase')
    item = models.ForeignKey('InventoryItem', related_name='purchase')
    user = models.ForeignKey('base.HackeratiUser', related_name='purchases')
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(decimal_places=2, max_digits=9)

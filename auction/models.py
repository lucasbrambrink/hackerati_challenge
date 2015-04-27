from django.db import models
from django.db.models import ImageField
from base.utils import FormatHelper as fh
from PIL import Image
from django.conf import settings
from StringIO import StringIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import requests
import os


class InventoryItem(models.Model):
    MAX_IMAGE_SIZE = 500

    image = models.ImageField(null=True)
    thumbnail = models.ImageField(null=True)
    name = models.CharField(max_length=50)
    description = models.TextField(null=True)
    reserved_price = models.DecimalField(decimal_places=2, max_digits=100)

    @property
    def is_sold(self):
        return len(self.item.all()) > 0


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

    def remove_same_name(self, name):
        for file in os.listdir(settings.MEDIA_ROOT):
            if file == name:
                path = os.path.join(settings.MEDIA_ROOT, file)
                os.remove(path)

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


class Purchase(models.Model):

    item = models.ForeignKey('InventoryItem', related_name='item')
    bought_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(decimal_places=2, max_digits=100)

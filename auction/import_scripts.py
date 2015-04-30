__author__ = 'lb'
from base.utils import FormatHelper as fh
from django.conf import settings
from bs4 import BeautifulSoup
from .models import InventoryItem, Auction
from base.models import HackeratiUser
from time import sleep
import pyimgur
import os
import requests
import re
import sys
import csv
import random

## REDIS QUEUE CALL
def sync_new_items_from_csv(user_id):
    importer = ImportHandler(user_id)
    importer.import_items_from_csv()
    return True



class ImportHandler(object):
    """
    Handles DB Import from
    """
    MAX_ITEMS = 10

    def __init__(self, user_id=None):
        self.user_id = int(user_id) if user_id and (type(user_id) is int or len(user_id)) else HackeratiUser.objects.first().id
        self.ic = ImgurClient()

    def upload_images_to_imgur(self):
        for item in InventoryItem.objects.all():
            link = self.ic.upload_to_imgur(item.image.path, item.name)
            item.path = link
            item.save()
        return None


    def import_items_from_csv(self, number_of_items=None):
        """
        :param number_of_items: max number of items to be imported
        :return: None, imports ``InventoryItem`` into DB for that user
        """
        if not number_of_items:
            number_of_items = self.MAX_ITEMS

        count_before = InventoryItem.objects.count()
        fieldnames = ['imgur_link', 'name', 'price']
        path = os.path.join(settings.MEDIA_ROOT, 'inventory_data.csv')
        with open(path, mode='r') as inventory_data:
            reader = csv.DictReader(inventory_data, fieldnames=fieldnames)
            for index, line in enumerate(reader):
                if index >= number_of_items:
                    break

                name = line['name']
                if InventoryItem.objects.filter(name__icontains=name).count() > 0:
                    # if this item is already in the data base, or one with a
                    # similar enough posting title, skip it but make to increment our counter
                    number_of_items += 1
                    continue

                item = InventoryItem(
                    user_id=self.user_id,
                    image_path=line['imgur_link'],
                    name=name,
                    reserved_price=line['price']
                )
                item.upload_image_from_path()
                item.save()


        created_num = InventoryItem.objects.count() - count_before
        print('created', created_num, 'new Items')
        return None


    def master_init_all_items(self):
        for item in InventoryItem.objects.all():
            if not item.is_being_auctioned:
                sleep(random.randint(15, 75))
                if not item.is_sold:
                    new_auction = Auction(
                        user_id=self.user_id,
                        hours_duration=random.randint(12, 24),
                        item=item,
                    )
                    new_auction.save()

    def initiate_auction_from_all_items(self, duration=1):
        try:
            duration = 1 if not len(duration) else int(duration)
            for item in InventoryItem.objects.filter(user_id=self.user_id):
                if not item.is_being_auctioned:
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




class AutoPopulateThroughCraigslist(object):
    BASELINK = "http://newyork.craigslist.org/"
    QUERY_ADDON = "search/sss?"
    HASPIC = 'hasPic=1'

    MINPRICE = 'minAsk='
    MAXPRICE = 'maxAsk='
    FILTERS = (
        (MINPRICE, 'min'),
        (MAXPRICE, 'max'),
    )

    def __init__(self, user_id=None, query='furniture', number_to_import=10, min_price='300', max_price='500'):
        self.user_id = user_id if user_id else HackeratiUser.objects.first().id
        self.query = query
        self.number_to_import = number_to_import
        self.min_price = min_price
        self.max_price = max_price
        self.ic = ImgurClient()


    ###---< Global Scrape Craigslist & Import to DB directly >---###
    def run_global_import(self, query='furniture', write_to_csv=True):
        """
        :param query: ``str`` to scrape results page for
        :return: ``bool`` indicating whether new objects were imported
        """
        soup = self.fetch_craigslist_page(filters={'min': self.min_price}, query=self.query)
        new_inventory_data = self.visit_each_posting(soup, num=self.number_to_import)
        if not len(new_inventory_data):
            return False

        count_before = InventoryItem.objects.count()

        for inventory in new_inventory_data:

            if InventoryItem.objects.filter(name__icontains=inventory[1]).count() > 0:
                # if an item already exists with a similar enough name, don't upload
                # to avoid duplication
                continue

            print('data', inventory)
            new_inventory = InventoryItem(
                image_url=inventory[0],
                name=inventory[1],
                reserved_price=float(inventory[2]),
                user_id=self.user_id
            )
            if new_inventory.upload_image_from_url():
                new_inventory.save()

            link = self.ic.upload_to_imgur(new_inventory.image.path, new_inventory.name)
            new_inventory.image_path = link
            new_inventory.save()


        if write_to_csv:
            self.write_to_csv()

        count_after = InventoryItem.objects.count()
        num_created = count_after - count_before
        print("Imported", num_created, "Objects")

        return True if num_created > 0 else False



    ###---< Helper Methods >---###
    def write_to_csv(self):
        """
        Writes all InventoryItems to CSV file with image file specified
        """
        data = InventoryItem.objects.all()
        fieldnames = ['imgur_link', 'name', 'price']
        file_path = os.path.join(settings.PROJECT_DIR, 'base', 'static', settings.MEDIA_ROOT, 'inventory_data.csv')
        with open(file_path, mode='w') as inventory:
            writer = csv.DictWriter(inventory, fieldnames=fieldnames, delimiter=',')
            for item in data:

                writer.writerow({
                    'imgur_link': item.image_path,
                    'name': item.name,
                    'price': item.reserved_price
                })


    def fetch_craigslist_page(self, filters={}, query=None):
        """
        :param filters: ``dict`` for min, max prices
        :param query: ``str`` search term for craigslist
        :return: ``bs4 instance`` of CL page
        """
        # build parameter string in proper format
        query_params = "&".join(filter[0] + filters[filter[1]] for filter in self.FILTERS if filter[1] in filters)

        final_query = "{base}{addon}{force_picture}{filters}{query}".format(
            base=self.BASELINK,
            addon=self.QUERY_ADDON,
            force_picture=self.HASPIC,
            filters=query_params,
            query=query
        )
        # http://newyork.craigslist.org/search/fua?hasPic=1&minAsk=200&maxAsk=300&query=furniture

        craiglist_page = requests.get(final_query)
        soup = BeautifulSoup(craiglist_page.content)
        return soup


    def visit_each_posting(self, soup=None, num=1):
        """
        :param soup: ``bs4 - instance``
        :param num: ``int`` maximum number of postings to visit
        :return: ``tuple`` triplets  of url, name, price extracted from each posting page
        """
        seen_links = []
        scraped_object_data = []
        for link in soup.findAll('a'):
            page_href = link.get('href')
            if page_href and re.search(r'\d{10}', page_href) and page_href not in seen_links:
                data = self.data_extract_from_page(page_url=page_href)
                if data.count(None) > 0:
                    # if any of the essential values are none, simply skip it
                    continue

                scraped_object_data.append(data)
                print(data)
                seen_links.append(page_href)
            if len(scraped_object_data) == num:
                break

        return scraped_object_data


    def data_extract_from_page(self, page_url=None):
        """ This is admitedly a little bit hacky (webscraping is never all that great)
            but it was a matter of getting the project to an interesting scale quickly

        :param page_url: ``str`` of posting to be visited & scraped
        :return: ``tuple`` triplet of image_url, name, price
        """
        page = requests.get(self.BASELINK + page_url)
        soup = BeautifulSoup(page.content)

        image_link = None
        for image in soup.findAll('img'):
            image_link_on_page = image.get('src')
            image_size = image_link_on_page.strip(".jpg")[-7:]
            try:
                sizes = map(int, image_size.split('x'))
                if min(sizes) > 300:
                    image_link = image_link_on_page
            except ValueError:
                pass

        name, price = None, None
        for title in soup.findAll('h2'):
            # print(title)
            for span in title.findAll('span'):
                if not len(span):
                    continue

                text = span.text
                if text[0] == '$':
                    price = text[1:]
                else:
                    name_uninspected = text.split(' - ')[0]
                    if name_uninspected and len([x for x in name_uninspected if not x.isalpha()]) < 5:
                        # if the title contains too many non-alphanumeric characters,
                        # it probably has annoying formatting and we can simply skip it
                        # since we don't have to be discerning here
                        name = fh.capitalize(phrase=name_uninspected)
                        name = name.strip('For Sale') # this fails nice and silently

        return image_link, name, price

class ImgurClient:
    CLIENT_ID = "311f8bd011b0b50"

    def __init__(self):
        self.im = pyimgur.Imgur(self.CLIENT_ID)

    def read_imgur(self, name):
        """
        :param name: ``str`` of imgur key
        :return: ``pyimgur Imgur`` instance
        """
        image = self.im.get_image(name)
        return image

    def upload_to_imgur(self, path, title):
        """
        :param path: ``str`` to file path
        :param title:  ``str`` to title uploaded image
        :return link: ``str``
        """
        im = pyimgur.Imgur(self.CLIENT_ID)
        uploaded_image = im.upload_image(path, title=title)
        return uploaded_image.link


if __name__ == "__main__":
    from django.core.management import setup_environ
    from auction_hackerati import settings
    setup_environ(settings)

    user_id = sys.argv[1]
    importer = AutoPopulateThroughCraigslist(user_id)
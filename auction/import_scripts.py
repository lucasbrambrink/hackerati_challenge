__author__ = 'lb'
from base.utils import FormatHelper as fh
from bs4 import BeautifulSoup
from .models import InventoryItem
import requests
import re



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

    def __init__(self, user_id=1, query='furniture', number_to_import=10, min_price='300', max_price='500'):
        self.user_id = user_id
        self.query = query
        self.number_to_import = number_to_import
        self.min_price = min_price
        self.max_price = max_price


    ###---< Global Scrape for Query >---###
    def run_global_import(self, query='furniture'):
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

        count_after = InventoryItem.objects.count()
        num_created = count_after - count_before
        print("Imported", num_created, "Objects")

        return True if num_created > 0 else False



    ###---< Helper Methods >---###
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

        return image_link, name, price





__author__ = 'lb'
from bs4 import BeautifulSoup
from .models import InventoryItem
import requests
import re



class AutoPopulateThroughCraigslist(object):
    BASELINK = "http://newyork.craigslist.org/"
    QUERY_ADDON = "search/fua?"
    HASPIC = 'hasPic=1'

    MINPRICE = 'minAsk='
    MAXPRICE = 'maxAsk='
    FILTERS = (
        (MINPRICE, 'min'),
        (MAXPRICE, 'max'),
    )

    def __init__(self, query='furniture', number_to_import=10, min_price='300', max_price='500'):
        self.query = query
        self.number_to_import = number_to_import
        self.min_price = min_price
        self.max_price = max_price


    def run_global_import(self, query='furniture'):
        soup = self.fetch_craigslist_page(filters={'min': self.min_price}, query=self.query)
        new_inventory_data = self.visit_each_posting(soup, num=self.number_to_import)

        for inventory in new_inventory_data:
            if inventory.count(None) > 0:
                # if any of the essential values are none, simply skip it
                continue

            if InventoryItem.objects.count(name__icontains=inventory[1]) > 0:
                # if an item already exists with a similar enough name, don't upload
                # to avoid duplication
                continue

            new_inventory = InventoryItem(
                image_url=inventory[0],
                name=inventory[1],
                reserved_price=float(inventory[2])
            )
            new_inventory.save()
            new_inventory.upload_image_from_url()

        return True

    def fetch_craigslist_page(self, filters={}, query=None):
        """
        :param filters:
        :param query:
        :return:
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
        count = 0
        seen_links = []
        scraped_object_data = []
        for link in soup.findAll('a'):
            page_href = link.get('href')
            if page_href and re.search(r'\d{10}', page_href) and page_href not in seen_links:
                data = self.data_extract_from_page(page_url=page_href)
                scraped_object_data.append(data)
                seen_links.append(page_href)
                print(data)
                count += 1
            if count == num:
                break

        return scraped_object_data


    def data_extract_from_page(self, page_url=None):
        """ This is admitedly a little bit hacky (webscraping is never all that great)
            but it was a matter of getting the project to an interesting scale quickyl

        :param page_url:
        :return:
        """
        page = requests.get(self.BASELINK + page_url)
        soup = BeautifulSoup(page.content)

        image_link = None
        for image in soup.findAll('img'):
            image_link = image.get('src')

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
                    if len([x for x in name_uninspected if not x.isalpha()]) < 5:
                        # if the title contains too many non-alphanumeric characters,
                        # it probably has annoying formatting and we can simply skip it
                        # since we don't have to be discerning here
                        name = name_uninspected

        return image_link, name, price


    def build_inventory_object(self, ):
        pass





__author__ = 'lb'
from bs4 import BeautifulSoup
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


    def run_global_import(self, num=10):
        soup = self.fetch_craigslist_page(filters={'min': '300'}, query='furniture')
        self.visit_each_posting(soup, num=10)

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
                    name = text.split(' - ')[0]

        return image_link, name, price


    def build_inventory_object(self, ):
        pass





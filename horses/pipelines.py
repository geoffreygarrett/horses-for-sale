# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from .google_api import get_coordinates, get_driving_time, get_formatted_address

class JunkmailPipeline:

    # get my latitude and longitude
    orig_coordinates = get_coordinates("Kleinmond, South Africa")

    def process_item(self, item, spider):

        # convert to datetime object with utc aware
        date = item['details']['Published']
        date = date.split('/')
        date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
        item['listing_date'] = date

        # get the address from the listing
        if 'Region' in item['details']:
            location = item['details']['Region']
            item['location'] = get_formatted_address(location)

            # get the coordinates from geoencode
            dest_coordinates = get_coordinates(location)
            item['coordinates'] = dest_coordinates

            # get the driving time from the coordinates
            driving_time = get_driving_time(
                list(self.orig_coordinates.values()), 
                list(dest_coordinates.values()))

            # add the driving time to the listing
            item['driving_time'] = driving_time / 3600

        return item

import re 
import datetime 

class EquinesaPipeline:

    # get my latitude and longitude
    orig_coordinates = get_coordinates("Kleinmond, South Africa")

    def process_item(self, item, spider):

        # get the address from the listing
        if 'location' in item:
            location = item['location']
            item['location'] = get_formatted_address(location)

            # get the coordinates from geoencode
            dest_coordinates = get_coordinates(location)
            item['coordinates'] = dest_coordinates

            # get the driving time from the coordinates
            driving_time = get_driving_time(
                list(self.orig_coordinates.values()), 
                list(dest_coordinates.values()))

            # add the driving time to the listing
            item['driving_time'] = driving_time / 3600

        if 'DOB / Age' in item['details']:
            date = item['details']['DOB / Age']
            re_age_1 = r"(\d+)\s?[yY]ears"
            re_age_2 = r"(20\d{2})"
            
            # if match group 1 
            match_1 = re.findall(re_age_1, date)
            match_2 = re.findall(re_age_2, date)
            if match_1:
                item['age'] = int(match_1[0])
                # if group 1
            elif match_2:
                # get current year
                current_year = datetime.datetime.now().year
                item['age'] = current_year - int(match_2[0])
            else:
                raise ValueError("No age found, {}: {}, {}".format(date, match_1, match_2))

        # convert listing date in format '31/08/2021' to datetime
        if 'listing_date' in item:
            date = item['listing_date']
            date = date.split('/')
            date = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
            item['listing_date'] = date
                
        return item


class HorsesPipeline:

    def process_item(self, item, spider):

        # currency + price format found
        re_currency_price = r"([\w]+)\s+?([\d\.\,\s]+)"
        match = re.findall(re_currency_price, item['price'])
        if match:
            item['price'] = match[0][1].strip()
            item['price'] = item['price'].replace(',', '')
            item['price'] = item['price'].replace(' ', '')
            item['currency'] = match[0][0]

            # convert to ZAR
            if item['currency'] == 'NAD':
                item['price'] = float(item['price']) * 1.14
                item['currency'] = 'ZAR'
            
            elif item['currency'] == 'ZAR' or item['currency'] == 'R':
                item['price'] = float(item['price'])
                item['currency'] = 'ZAR'

            else:
                item['price'] = float(item['price'])

        return item

class MongoPipeline:
    # def process_item(self, item, spider):
    #     return item
    collection_name = 'testing'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item



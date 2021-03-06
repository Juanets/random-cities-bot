import os
import time
import shutil
import random
import requests
from config import *
from geopy.geocoders import Nominatim
from googleapiclient.discovery import build

class Geo():
    """Generate random coordinates and use geopy to get the address."""
    def __init__(self):
        self.geolocator = Nominatim()

    def coordinates(self):
        print('Generating coordinates...')
        lat = random.uniform(0, 90)
        lon = random.uniform(0, 180)
        coord = '{lat}, {lon}'.format(lat=lat, lon=lon)
        return coord

    def get_location(self):
        try:
            coordinates = self.coordinates()
            print('Deciphering coordinates...')
            geo = self.geolocator.reverse(coordinates, language='en')

            # activate recursion if coordinates land on unknown territory
            if geo.address is None:
                return self.get_location()

            address = geo.raw['address']
            country = address['country']

            if 'city' in address:
                city = address['city']
            elif 'city_district' in address:
                city = address['city_district']
            elif 'county' in address:
                city = address['county']
            elif 'state_district' in address:
                city = address['state_district']
            else:
                city = None

            if city is None:
                return country
            else:
                location = '{city}, {country}'.format(city=city, country=country)
                return location
        except Exception as e:
            print(e)

class Google():
    """Using a Google Custom Search Engine (CSE) that returns four (4) images."""
    def __init__(self):
        self.service = build("customsearch", "v1", developerKey=devKey)

    def search(self, place):
        try:
            print('Searching images...')
            results = self.service.cse().list(
                q=place,
                num=num,
                searchType=searchType,
                imgType=imgType,
                cx=cx
            ).execute()

            # return list of urls (4)
            urls = [url['link'] for url in results['items']]
            return urls

        except Exception as e:
            return e


class ImageManager():
    """Using requests to download the four images obtained from the CSE
    and save them to ./images; and delete them with self.delete().
    """
    def __init__(self):
        self.path = 'images/'
        self.default_image_name = 'images/{}.jpg'

    def save(self, urls):
        image_names = []
        print('Saving images...')
        for url in urls:
            try:
                name = self.rename()
                image_names.append(name)
                pic = requests.get(url, stream=True)
                with open(name, 'wb') as out_file:
                    shutil.copyfileobj(pic.raw, out_file)
            except Exception as e:
                print(e)

        return image_names

    def delete(self):
        try:
            print('Cleaning image directory...')
            for image in os.listdir(self.path):
                image_path = os.path.join(self.path, image)
                os.unlink(image_path)
        except Exception as e:
            print(e)

    def rename(self):
        time.sleep(1)
        return self.default_image_name.format(int(time.time()))

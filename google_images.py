import os
import time
import shutil
import requests
from config import *
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

# get random cities
class Scrapy():

    def get_random_city(self):
        try:
            r = requests.get('https://www.randomlists.com/random-location')
            soup = BeautifulSoup(r.content, 'html.parser')
            city = soup.find('span', class_='subtle').get_text()
            print(city)
            return city
        except Exception as e:
            print(e)

# google image search (random city)
class Google():

    def __init__(self):
        self.service = build("customsearch", "v1", developerKey=devKey)

    def search(self, place):
        try:
            results = self.service.cse().list(
                q=place,
                num=num,
                searchType=searchType,
                imgType=imgType,
                cx=cx
            ).execute()

            # return list of urls (4)
            return [url['link'] for url in results['items']]

        except Exception as e:
            return e


# save and delete images
class ImageManager():

    def __init__(self):
        self.path = 'images/'
        self.default = 'images/{}.jpg'

    def save(self, urls):
        image_names = []
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
        for image in os.listdir(self.path):
            image_path = os.path.join(self.path, image)
            try:
                os.unlink(image_path)
            except Exception as e:
                print(e)

    def rename(self):
        time.sleep(1)
        return self.default.format(int(time.time()))
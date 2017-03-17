import os
import time
import shutil
import requests
from config import *
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

class Crawler():
    """Using requests and bs4 to get a random location from randomlists.com."""
    def get_random_city(self):
        try:
            r = requests.get('https://www.randomlists.com/random-location')
            soup = BeautifulSoup(r.content, 'html.parser')
            city = soup.find('span', class_='subtle').get_text()
            print(city)
            return city
        except Exception as e:
            print(e)


class Google():
    """Using a Google Custom Search Engine (CSE) that returns four (4) images."""
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
        return self.default_image_name.format(int(time.time()))

import time
import schedule
from twitter import TwitterAPI
from images import Google, ImageManager, Crawler

def go():

	# get random city
	city = Crawler().get_random_city()

	# get 4 images (urls)
	urls = Google().search(city)

	# save images
	image_names = ImageManager().save(urls)

	# tweet 'em
	TwitterAPI().compose(city, image_names)

	# clean image directory
	ImageManager().delete()

# run every 2 hours
schedule.every(2).hours.do(go)

while True:
	schedule.run_pending()
	time.sleep(1)

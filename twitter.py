import tweepy
from config import *

class TwitterAPI():
	def __init__(self):
		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(auth)

	def compose(self, city, images):
		try:
			print('Uploading images to Twitter...')
			media_ids = [self.api.media_upload(i).media_id_string for i in images]
			tweet = city + ' #Travel'

			print('Tweeting...')
			self.api.update_status(tweet, media_ids=media_ids)

			return True
		except Exception as e:
			print(e)
			return False

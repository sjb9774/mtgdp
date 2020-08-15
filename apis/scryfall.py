import datetime
import time
import requests


class ScryfallApi:

	API_URL = 'https://api.scryfall.com/'

	def __init__(self):
		self.last_request_timestamp = 0
		self.request_spacing = .1

	def request_api(self, *args, **kwargs):
		now = datetime.datetime.now()
		now_timestamp = now.timestamp()
		diff = now_timestamp - self.last_request_timestamp
		if diff <= self.request_spacing:
			time.sleep(.1 - self.request_spacing)
			self.last_request_timestamp = datetime.datetime.now().timestamp()
		return requests.get(*args, **kwargs)

	def search(self, query):
		return self.request_api(f'{self.API_URL}/cards/search', params={'q': query}).json()
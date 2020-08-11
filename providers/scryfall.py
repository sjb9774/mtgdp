from providers.provider import PriceProvider
from product.pricing import CardPriceSnapshot, CardPricing
from product.identity import CardIdentity
from typing import List
import requests
import time
import datetime


class ScryfallPricing(PriceProvider):

	def __init__(self):
		super().__init__()
		self.last_request_timestamp = 0
		self.request_spacing = .1

	def get_price_categories(self):
		return ['usd', 'usd_foil']

	def get_pricing(
		self,
		card_name=None,
		card_set=None,
		multiverse_id=None,
		printing_id=None,
		**kwargs
	) -> List[CardPriceSnapshot]:
		now = datetime.datetime.now()
		query = ''
		if card_name:
			query += f"{card_name}"
		if card_set:
			query += f" set:{card_set}"
		if printing_id:
			query += f" number:{printing_id}"
		cards = []
		response = self.request_api('https://api.scryfall.com/cards/search', params={
			'q': query,
		}).json()
		cards.extend(response.get('data'))
		while response.get('next_page'):
			response = self.request_api(response.get('next_page')).json()
			cards.extend(response.get('data'))
		prices = []
		for card in cards:
			if card.get('prices', {}).get('usd'):
				normal_pricing = CardPricing(market_price=card.get('prices', {}).get('usd'))
				normal_identity = CardIdentity(
					set_code=card.get('set'),
					collector_number=card.get('collector_number'),
					foil=False,
					name=card.get('name')
				)
				prices.append(CardPriceSnapshot(identity=normal_identity, pricing=normal_pricing, timestamp=now))
			if card.get('prices', {}).get('usd_foil'):
				foil_identity = CardIdentity(
					set_code=card.get('set'),
					collector_number=card.get('collector_number'),
					foil=True,
					name=card.get('name')
				)
				foil_pricing = CardPricing(market_price=card.get('prices', {}).get('usd_foil'))
				prices.append(CardPriceSnapshot(identity=foil_identity, pricing=foil_pricing, timestamp=now))

		return prices

	def request_api(self, *args, **kwargs):
		now = datetime.datetime.now()
		now_timestamp = now.timestamp()
		diff = now_timestamp - self.last_request_timestamp
		if diff <= self.request_spacing:
			time.sleep(.1 - self.request_spacing)
			self.last_request_timestamp = datetime.datetime.now().timestamp()
		return requests.get(*args, **kwargs)

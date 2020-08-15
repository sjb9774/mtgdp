from providers.provider import PriceProvider
from product.pricing import CardPriceSnapshot, CardPricing
from product.identity import CardIdentity
from apis.scryfall import ScryfallApi
from typing import List
import datetime


class ScryfallPricing(PriceProvider):

	def __init__(self):
		super().__init__()
		self.last_request_timestamp = 0
		self.request_spacing = .1
		self.client = ScryfallApi()

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
		response = self.client.search(query)

		prices = []

		while True:
			cards = response.get('data')
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
			if not response.get('next_page'):
				break
			response = self.client.request_api(response.get('next_page')).json()

		return prices



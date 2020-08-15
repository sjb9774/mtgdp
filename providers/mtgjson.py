from providers.provider import PriceProvider
from apis.mtgjson import MtgJsonApiClient
from product.identity import CardIdentity
from product.pricing import CardPricing, CardPriceSnapshot
from typing import List
import datetime


class MtgJsonPricing(PriceProvider):
	"""
	Technically MTGJSON just aggregates prices from _other_ providers, but we can still logically treat it
	like a pricing provider itself
	"""

	def __init__(self, source: str = None, pricing_type: str = None, debug: bool = False):
		super().__init__()
		self.source = source
		if pricing_type not in ['buylist', 'retail']:
			raise Exception(f'pricing_type must being "buylist" or "retail", was {pricing_type}')
		self.pricing_type = pricing_type
		self.debug = debug

	def ouput(self, message):
		if self.debug:
			print(message)

	def get_pricing(
		self,
		card_name=None,
		card_set=None,
		multiverse_id=None,
		printing_id=None,
		**kwargs) -> List[CardPriceSnapshot]:
		refresh_prices = kwargs.get('refresh_prices', False)
		refresh_printings = kwargs.get('refresh_printings', False)

		client = MtgJsonApiClient(version='5')
		all_prices = client.get_all_prices(force_refresh=refresh_prices)
		all_printings = client.get_all_printings(force_refresh=refresh_printings)
		cards = all_printings.get('data', {}).get(card_set.upper(), {}).get('cards')
		snapshots = []
		skipped = 0
		for card in cards:
			self.ouput(f'Fetching {card.get("name")}..')
			price_data = all_prices
			for criterion in ('data', card.get('uuid'), 'paper', self.source, self.pricing_type):
				if not price_data.get(criterion):
					self.ouput(f"'{card.get('name')}' : Couldn't find data for '{criterion}' while fetching prices")
					price_data = None
					break
				price_data = price_data.get(criterion)
			if not price_data:
				self.ouput(f"Skipping {card.get('name')}")
				skipped += 1
				continue
			normal_prices = price_data.get('normal', {})
			for date_str, normal_price in normal_prices.items():
				date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
				normal_card_identity = CardIdentity(
					name=card.get('name'),
					collector_number=card.get('number'),
					set_code=card_set.upper(),
					foil=False
				)
				normal_pricing = CardPricing(market_price=normal_price)
				normal_snapshot = CardPriceSnapshot(
					pricing=normal_pricing,
					identity=normal_card_identity,
					timestamp=date
				)
				snapshots.append(normal_snapshot)

			foil_prices = price_data.get('foil', {})
			for date_str, foil_price in foil_prices.items():
				date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
				foil_card_identity = CardIdentity(
					name=card.get('name'),
					collector_number=card.get('number'),
					set_code=card_set.upper(),
					foil=True
				)
				foil_pricing = CardPricing(market_price=foil_price)
				foil_snapshot = CardPriceSnapshot(pricing=foil_pricing, identity=foil_card_identity, timestamp=date)
				snapshots.append(foil_snapshot)

		return snapshots

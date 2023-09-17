from providers.provider import PriceProvider
from product.identity import CardIdentity
from product.pricing import CardPricing, CardPriceSnapshot
from apis import tcgplayer
import json
import datetime
from typing import List


class TcgPlayerPricing(PriceProvider):

	def __init__(self):
		super().__init__()
		self.groups = {}
		self.public_key = None
		self.private_key = None
		self.bearer_token = None

	def set_credentials(self):
		credentials = self.read_credentials()
		self.public_key = credentials.get('public_key')
		self.private_key = credentials.get('private_key')
		self.groups = {}

	def read_credentials(self) -> dict:
		with open('credentials/tcgplayer.json', 'r') as f:
			cred_data = json.loads(f.read())
		return cred_data

	def get_pricing(
		self,
		card_name: str="",
		card_set: str="",
		multiverse_id: str="",
		printing_id: str="",
		**kwargs
	) -> List[CardPriceSnapshot]:
		if not self.public_key:
			self.set_credentials()
		now = datetime.datetime.now()
		all_groups = self.get_all_groups()
		specified_group = all_groups.get(card_set.upper())
		if not specified_group:
			raise Exception(f'Could not find information for set "{card_set}"')
		tcg_group_id = specified_group.get("groupId")
		set_cards = self.get_group_items(tcg_group_id)
		products_map = {}
		for card in set_cards:
			products_map[card.get('productId')] = card
		set_pricing = self.get_group_pricing(tcg_group_id)
		pricing = []
		for price in set_pricing.get('results', []):
			if products_map.get(price.get('productId')):
				product = products_map[price.get('productId')]
				collector_number = None
				for data in product.get('extendedData'):
					if data.get('name') == 'Rarity' and data.get('value') == 'T':
						# tokens can share collector's numbers with cards, which goofs up graphs :(
						collector_number = None
						break
					if data.get('name') == 'Number':
						collector_number = data.get('value')

				identity = self.get_card_identity(
					name=product.get('name'),
					collector_number=collector_number,
					set_code=card_set,
					foil=price.get('subTypeName') and price.get('subTypeName').lower() == 'foil'
				)
				card_pricing = self.get_card_pricing(
					low_price=price.get('lowPrice'),
					mid_price=price.get('midPrice'),
					high_price=price.get('highPrice'),
					market_price=price.get('marketPrice'),
				)
				snapshot = CardPriceSnapshot(pricing=card_pricing, identity=identity, timestamp=now)
				pricing.append(snapshot)
		return pricing

	def get_group_pricing(self, group_id: int) -> dict:
		prices = tcgplayer.send_request(
			f'pricing/group/{group_id}',
			http_method='GET',
			headers={'Authorization': f'Bearer {self.get_token()}'},
			versioned=False
		)
		return prices

	def get_group_items(self, group_id: int) -> List[dict]:
		set_cards = self.auto_paginate(
			'catalog/products',
			http_method='GET',
			headers={'Authorization': f'Bearer {self.get_token()}'},
			versioned=False,
			query_params={
				'groupId': group_id,
				'categoryId': 1,
				'getExtendedFields': True
			}
		)
		card_objects = []
		for cards_results in set_cards:
			card_objects.extend(cards_results.get('results'))
		return card_objects

	def auto_paginate(self, *args, **kwargs) -> list:
		responses = []
		offset = 0
		limit = 100
		while True:
			q_params = kwargs.pop('query_params', {})
			q_params['offset'] = offset
			q_params['limit'] = limit
			kwargs['query_params'] = q_params
			response = tcgplayer.send_request(*args, **kwargs)
			if not response.get('results'):
				break
			responses.append(response)
			offset += limit
			if offset >= response.get('totalItems'):
				break
		return responses

	def get_token(self) -> str:
		if not self.bearer_token:
			self.bearer_token = tcgplayer.get_bearer_token(public_key=self.public_key, private_key=self.private_key)
		return self.bearer_token.get_value()

	def get_all_groups(self) -> dict:
		if not self.groups:
			all_responses = self.auto_paginate(
				'catalog/categories/1/groups',
				versioned=False,
				http_method='GET',
				headers={'Authorization': f'Bearer {self.get_token()}'}
			)
			for response in all_responses:
				group_info = response.get('results')
				for group in group_info:
					self.groups[group.get('abbreviation', group.get('name'))] = group
		return self.groups

	def get_card_identity(self, name=None, collector_number=None, set_code=None, foil=None) -> CardIdentity:
		identity = CardIdentity(name=name, collector_number=collector_number, set_code=set_code, foil=foil)
		return identity

	def get_card_pricing(
		self,
		low_price: float = None,
		mid_price: float = None,
		high_price: float = None,
		market_price: float = None
	) -> CardPricing:
		pricing = CardPricing(
			low_price=low_price,
			mid_price=mid_price,
			high_price=high_price,
			market_price=market_price,
			provider="tcgplayer"
		)
		return pricing


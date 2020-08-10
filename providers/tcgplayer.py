from providers.provider import PriceProvider
from apis import tcgplayer
import json


class TcgPlayerPricing(PriceProvider):

	def __init__(self):
		super().__init__()
		credentials = self.read_credentials()
		self.public_key = credentials.get('public_key')
		self.private_key = credentials.get('private_key')
		self.groups = {}
		self.bearer_token = None

	def read_credentials(self):
		with open('credentials/tcgplayer.json', 'r') as f:
			cred_data = json.loads(f.read())
		return cred_data

	def get_pricing(self, card_name=None, card_set=None, multiverse_id=None, printing_id=None, **kwargs):
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
		for price in set_pricing.get('results'):
			if products_map.get(price.get('productId')):
				pricing.append({
					'tcgplayer_id': price.get('productId'),
					'name': products_map[price.get('productId')].get('name'),
					'set_code': card_set,
					'tcgplayer_group_id': tcg_group_id,
					'pricing': price
				})
		return pricing

	def get_group_pricing(self, group_id):
		prices = tcgplayer.send_request(
			f'pricing/group/{group_id}',
			http_method='GET',
			headers={'Authorization': f'Bearer {self.get_token()}'},
			versioned=False
		)
		return prices

	def get_group_items(self, group_id):
		set_cards = self.auto_paginate(
			'catalog/products',
			http_method='GET',
			headers={'Authorization': f'Bearer {self.get_token()}'},
			versioned=False,
			query_params={'groupId': group_id, 'categoryId': 1}
		)
		card_objects = []
		for cards_results in set_cards:
			card_objects.extend(cards_results.get('results'))
		return card_objects

	def auto_paginate(self, *args, **kwargs):
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

	def get_token(self):
		if not self.bearer_token:
			self.bearer_token = tcgplayer.get_bearer_token(public_key=self.public_key, private_key=self.private_key)
		return self.bearer_token.get_value()

	def get_all_groups(self):
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


class ProductPricing:

	def __init__(self, price_types=None, pricing=None):
		self.pricing = {}
		self.price_types = price_types[:]
		for price_type in self.price_types:
			self.pricing[price_type] = pricing.get(price_type)

	def get_price(self, price_type):
		return self.pricing.get(price_type)

	def set_price(self, price_type, price):
		if price_type in self.price_types:
			self.price_types[price_type] = price
		else:
			raise Exception(f'Price type "{price_type}" does not exist in "{repr(self)}"')

	def get_pricing(self):
		return self.pricing


class CardPricing(ProductPricing):

	def __init__(self, market_price=None, low_price=None, mid_price=None, high_price=None):
		pricing = {
			'market_price': market_price,
			'low_price': low_price,
			'high_price': high_price,
			'mid_price': mid_price
		}
		super().__init__(price_types=pricing.keys(), pricing=pricing)

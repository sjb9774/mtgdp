from product.identity import ProductIdentity, CardIdentity
import datetime


class ProductPricing:

	def __init__(self, price_types: list = None, pricing: dict = None):
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

	def __init__(
		self,
		market_price: float = None,
		low_price: float = None,
		mid_price: float = None,
		high_price: float = None
	):
		pricing = {
			'market_price': market_price,
			'low_price': low_price,
			'high_price': high_price,
			'mid_price': mid_price
		}
		super().__init__(price_types=list(pricing.keys()), pricing=pricing)


class PriceSnapshot:

	def __init__(
		self,
		pricing: ProductPricing = None,
		identity: ProductIdentity = None,
		timestamp: datetime.datetime = None
	):
		self.pricing = pricing
		self.identity = identity
		self.timestamp = timestamp

	def get_pricing(self) -> ProductPricing:
		return self.pricing

	def get_identity(self) -> ProductIdentity:
		return self.identity

	def get_timestamp(self) -> datetime.datetime:
		return self.timestamp


class CardPriceSnapshot(PriceSnapshot):

	def __init__(
		self,
		pricing: CardPricing = None,
		identity: CardIdentity = None,
		timestamp: datetime.datetime = None
	):
		self.pricing = pricing
		self.identity = identity
		self.timestamp = timestamp
		super().__init__(pricing=pricing, identity=identity, timestamp=timestamp)

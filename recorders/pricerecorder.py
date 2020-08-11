from product.identity import ProductIdentity, CardIdentity
from product.pricing import ProductPricing, CardPricing


class PriceRecorder:

	def __init__(self):
		pass

	def record_price(self, product_identity: ProductIdentity, product_pricing: ProductPricing):
		pass


class JSONCardPriceRecorder(PriceRecorder):

	def record_price(self, product_identity: CardIdentity, pricing: CardPricing):
		identity = product_identity.get_identity()
		pricing = pricing.get_pricing()


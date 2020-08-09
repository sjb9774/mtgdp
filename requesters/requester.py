from providers.provider import PriceProvider


class Requester:

	def __init__(self, price_provider: PriceProvider):
		self.price_provider = price_provider

	def request_set_pricing(self, set_code):
		prices = self.price_provider.get_pricing(card_set=set_code)
		return prices

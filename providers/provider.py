from typing import List
from product.pricing import PriceSnapshot


class PriceProvider:

	def __init__(self):
		pass

	def get_price_categories(self) -> List[str]:
		return []

	def get_pricing(self, card_name=None, card_set=None, multiverse_id=None, printing_id=None, **kwargs) -> List[PriceSnapshot]:
		return []

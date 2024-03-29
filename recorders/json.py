from recorders.pricerecorder import PriceRecorder
from product.pricing import CardPriceSnapshot
from typing import List
from pathlib import Path
import json


class JSONCardPriceRecorder(PriceRecorder):

	def __init__(self, filepath: str = ""):
		super().__init__()
		self.filepath = filepath

	def record_prices(self, snapshots: List[CardPriceSnapshot] = []) -> List[dict]:
		data = []
		for snapshot in snapshots:
			data.append(self.dictify_single_price(snapshot))
		Path(self.filepath.rsplit('/', 1)[0]).mkdir(parents=True, exist_ok=True)
		with open(self.filepath, 'w+') as f:
			f.write(json.dumps(data))
		return data

	def dictify_single_price(self, snapshot: CardPriceSnapshot) -> dict:
		identity = snapshot.get_identity()
		pricing = snapshot.get_pricing()
		identity_dict = identity.get_identity()
		identity_dict['pricing'] = pricing.get_pricing()
		identity_dict['date'] = snapshot.get_timestamp().strftime('%Y-%m-%d %H:%M:%S')
		return identity_dict

	def __repr__(self) -> str:
		return f'<{self.__class__.__name__} writing to "{self.filepath}">'
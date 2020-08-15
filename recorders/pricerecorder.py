from product.identity import ProductIdentity, CardIdentity
from product.pricing import ProductPricing, CardPricing, CardPriceSnapshot, PriceSnapshot
from product.repository import CardSnapshotRepository
from typing import List
import json
from pathlib import Path


class PriceRecorder:

	def __init__(self):
		pass

	def record_prices(self, snapshots: List[PriceSnapshot]):
		pass


class JSONCardPriceRecorder(PriceRecorder):

	def __init__(self, filepath=None):
		super().__init__()
		self.filepath = filepath

	def record_prices(self, snapshots: List[CardPriceSnapshot] = None):
		data = []
		for snapshot in snapshots:
			data.append(self.dictify_single_price(snapshot))
		Path(self.filepath.rsplit('/', 1)[0]).mkdir(parents=True, exist_ok=True)
		with open(self.filepath, 'w+') as f:
			f.write(json.dumps(data))
		return data

	def dictify_single_price(self, snapshot: CardPriceSnapshot = None) -> dict:
		identity = snapshot.get_identity()
		pricing = snapshot.get_pricing()
		identity_dict = identity.get_identity()
		identity_dict['pricing'] = pricing.get_pricing()
		identity_dict['date'] = snapshot.get_timestamp().strftime('%Y-%m-%d %H:%M:%S')
		return identity_dict

	def __repr__(self):
		return f'<{self.__class__.__name__} writing to "{self.filepath}">'


class DBPriceRecorder(PriceRecorder):

	def record_prices(self, snapshots: List[CardPriceSnapshot]):
		repo = CardSnapshotRepository()
		for snapshot in snapshots:
			repo.save(snapshot)

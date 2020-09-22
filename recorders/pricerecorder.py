from product.identity import ProductIdentity, CardIdentity
from product.models.identity import CardIdentity as CardIdentityModel
from product.pricing import ProductPricing, CardPricing, CardPriceSnapshot, PriceSnapshot
from product.repositories.pricing import CardSnapshotRepository, CardPricingProviderRepository, CardIdentityRepository
from product.repositories.pricing import CardPricingTypeRepository, CardPricingRepository
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

	def __init__(self):
		super().__init__()
		self.snapshot_repo = CardSnapshotRepository()
		self.provider_repo = CardPricingProviderRepository()
		self.pricing_repo = CardPricingRepository()
		self.identity_repository = CardIdentityRepository()
		self.type_repo = CardPricingTypeRepository()

	def get_provider(self, name) -> CardIdentityModel:
		return self.provider_repo.manifest(name=name)

	def construct_identity(self, identity: CardIdentity) -> CardIdentityModel:
		identity = self.identity_repository.manifest(**identity.get_identity())
		return identity

	def construct_pricings(self, pricing: CardPricing):
		pricing_provider = self.provider_repo.manifest(name=pricing.provider)
		pricings = []
		for price_type, price in pricing.get_pricing().items():
			if price is not None:
				price_type = self.type_repo.manifest(type=price_type)
				pricing = self.pricing_repo.create(
					provider_id=pricing_provider.provider_id,
					price=price,
					pricing_type_id=price_type.pricing_type_id
				)
				pricings.append(pricing)
		return pricings

	def record_prices(self, snapshots: List[CardPriceSnapshot]):
		for snapshot in snapshots:
			identity = snapshot.get_identity()
			db_identity = self.construct_identity(identity)
			pricing = snapshot.get_pricing()
			db_pricings = self.construct_pricings(pricing)
			for pricing in db_pricings:
				self.snapshot_repo.manifest(
					pricing_id=pricing.pricing_id,
					identity_id=db_identity.identity_id,
					timestamp=snapshot.timestamp
				)

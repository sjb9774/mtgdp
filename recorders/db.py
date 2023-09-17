from product.identity import ProductIdentity, CardIdentity
from product.models.identity import CardIdentity as CardIdentityModel
from product.pricing import ProductPricing, CardPricing, CardPriceSnapshot, PriceSnapshot
from product.repositories.pricing import CardSnapshotRepository, CardPricingProviderRepository, CardIdentityRepository
from product.repositories.pricing import CardPricingTypeRepository, CardPricingRepository
from recorders.pricerecorder import PriceRecorder
from typing import List


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

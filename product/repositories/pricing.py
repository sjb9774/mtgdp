from product.pricing import CardPriceSnapshot, CardPricing as CardDataPricing, CardIdentity as CardDataIdentity
from product.models.pricing import CardPricing, CardPricingType, CardIdentity, CardPriceSnapshot as SnapshotModel
from product.models.pricing import CardPricingProvider
from product.repositories.base import Repository
from sqlalchemy.orm.exc import NoResultFound
from db import get_session


class CardPricingProviderRepository(Repository):

	def __init__(self):
		super().__init__(model_type=CardPricingProvider)

	def load_by_fields(self, name: str = None):
		return super().load_by_fields(name=name)

	def get_fields(self):
		return ['name']


class CardPricingTypeRepository(Repository):

	def __init__(self):
		super().__init__(model_type=CardPricingType)

	def load_by_fields(self, type: str = None):
		return super().load_by_fields(type=type)

	def get_fields(self):
		return ['type']


class CardIdentityRepository(Repository):

	def __init__(self):
		super().__init__(model_type=CardIdentity, identity_type=CardDataIdentity)

	def load_by_fields(self, name=None, set_code=None, foil=None, collector_number=None):
		return super().load_by_fields(name=name, set_code=set_code, foil=foil, collector_number=collector_number)


class CardPricingRepository(Repository):

	def __init__(self):
		super().__init__(model_type=CardPricing)

	def get_fields(self):
		return ['price', 'pricing_type_id', 'provider_id']


class CardSnapshotRepository(Repository):

	def __init__(self):
		super().__init__(model_type=SnapshotModel)

	def get_fields(self):
		return ['pricing_id', 'identity_id', 'timestamp']

from product.pricing import CardPriceSnapshot
from product.models.pricing import CardPricing, CardPricingType, CardIdentity, CardPriceSnapshot as SnapshotModel
from db import get_session


class CardSnapshotRepository:

	def save(self, snapshot: CardPriceSnapshot):
		identity_model = CardIdentity()
		identity_data = snapshot.get_identity().get_identity()
		identity_model.name = identity_data.get('name')
		identity_model.collector_number = identity_data.get('collector_number')
		identity_model.foil = identity_data.get('foil')
		identity_model.set_code = identity_data.get('set_code')

		session = get_session()
		for price_type, value in snapshot.get_pricing().get_pricing().items():
			if value is None:
				continue
			pricing_type = CardPricingType()
			pricing_type.type = price_type

			pricing_model = CardPricing()
			pricing_model.price = value
			pricing_model.pricing_type = pricing_type

			empty_snapshot_model = SnapshotModel()
			empty_snapshot_model.pricing = pricing_model
			empty_snapshot_model.identity = identity_model
			empty_snapshot_model.timestamp = snapshot.timestamp
			session.add(empty_snapshot_model)
		session.commit()
		session.flush()

	def load(self, snapshot_id):
		pass

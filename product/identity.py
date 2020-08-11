class ProductIdentity:

	def get_identifying_fields(self):
		return []

	def get_identity(self):
		identity = {}
		for field in self.get_identifying_fields():
			identity[field] = getattr(self, field) if hasattr(self, field) else None
		return identity


class CardIdentity(ProductIdentity):

	def __init__(self, name=None, collector_number=None, set_code=None, foil=None):
		self.name = name
		self.set_code = set_code
		self.collector_number = collector_number
		self.foil = foil

	def get_identifying_fields(self):
		return ['collector_number', 'set_code', 'name', 'foil']


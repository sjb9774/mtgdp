from db import Base, get_session
from product.identity import ProductIdentity
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import raiseload
from typing import Type


class Repository:

	def __init__(self, model_type: Type[Base] = None, identity_type: Type[ProductIdentity] = None):
		self.model_type = model_type
		self.identity_type = identity_type
		self.active_session = None

	def load_by_id(self, entity_id: int = None):
		session = get_session()
		result = session.query(self.model_type).get(entity_id)
		session.close()
		return result

	def load_by_fields(self, **kwargs) -> Base:
		session = get_session()
		try:
			result = session.query(self.model_type).filter_by(**kwargs).options(raiseload('*')).one()
		except NoResultFound:
			session.close()
			return None
		session.commit()
		session.close()
		return result

	def get_fields(self):
		return self.identity_type.get_identifying_fields()

	def manifest(self, **kwargs) -> Base:
		result = self.load_by_fields(**kwargs)
		if not result:
			result = self.create(**kwargs)
		return result

	def create(self, **kwargs) -> Base:
		new_object = self.model_type()
		for identifying_field in self.get_fields():
			setattr(new_object, identifying_field, kwargs.get(identifying_field))
		self.save(new_object)
		return new_object

	def save(self, model: Base) -> Base:
		session = get_session()
		session.add(model)
		session.commit()
		session.flush()
		session.close()
		return model


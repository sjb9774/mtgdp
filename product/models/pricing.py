from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from product.models.identity import CardIdentity
from db import Base


class CardPricingType(Base):

	__tablename__ = 'card_pricing_type'
	pricing_type_id = Column(Integer, primary_key=True)
	type = Column(String(255))
	prices = relationship("CardPricing", back_populates="pricing_type")


class CardPricing(Base):

	__tablename__ = 'card_pricing'
	pricing_id = Column(Integer, primary_key=True)
	price = Column(Float)
	pricing_type_id = Column(Integer, ForeignKey(f'{CardPricingType.__tablename__}.pricing_type_id'))

	snapshots = relationship("CardPricingSnapshot", back_populates="pricing")
	pricing_type = relationship("CardPricingType", back_populates="prices")


class CardPricingSnapshot(Base):

	__tablename__ = 'card_pricing_snapshot'
	snapshot_id = Column(Integer, primary_key=True)
	pricing_id = Column(Integer, ForeignKey(f'{CardPricing.__tablename__}.pricing_id'))
	identity_id = Column(Integer, ForeignKey(f'{CardIdentity.__tablename__}.identity_id'))
	timestamp = Column(DateTime)

	pricing = relationship("CardPricing", back_populates="snapshots")
	identity = relationship("CardIdentity", back_populates="snapshots")

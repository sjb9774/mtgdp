from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from product.models.identity import CardIdentity
from db import Base


class CardPricingType(Base):

	__tablename__ = 'card_pricing_type'
	pricing_type_id = Column(Integer, primary_key=True)
	type = Column(String(255), unique=True)

	prices = relationship("CardPricing", back_populates="pricing_type", lazy="joined")


class CardPricing(Base):

	__tablename__ = 'card_pricing'
	pricing_id = Column(Integer, primary_key=True)
	price = Column(Float)
	pricing_type_id = Column(Integer, ForeignKey(f'{CardPricingType.__tablename__}.pricing_type_id'))
	provider_id = Column(Integer, ForeignKey('card_pricing_provider.provider_id'))

	snapshots = relationship("CardPriceSnapshot", back_populates="pricing", cascade="all, delete-orphan", lazy="joined")
	pricing_type = relationship("CardPricingType", back_populates="prices", lazy="joined")
	provider = relationship("CardPricingProvider", back_populates="prices", lazy="joined")


class CardPriceSnapshot(Base):

	__tablename__ = 'card_pricing_snapshot'
	snapshot_id = Column(Integer, primary_key=True)
	pricing_id = Column(Integer, ForeignKey(f'{CardPricing.__tablename__}.pricing_id'))
	identity_id = Column(Integer, ForeignKey(f'{CardIdentity.__tablename__}.identity_id'))
	timestamp = Column(DateTime)

	pricing = relationship("CardPricing", back_populates="snapshots", lazy="joined")
	identity = relationship("CardIdentity", back_populates="snapshots", lazy="joined")


class CardPricingProvider(Base):

	__tablename__ = 'card_pricing_provider'
	provider_id = Column(Integer, primary_key=True)
	name = Column(String(255), unique=True)

	prices = relationship("CardPricing", back_populates="provider", lazy="joined")

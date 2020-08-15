from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db import Base


class CardIdentity(Base):

	__tablename__ = 'card_identity'
	identity_id = Column(Integer, primary_key=True)
	name = Column(String(255))
	set_code = Column(String(255))
	collector_number = Column(String(255))
	foil = Column(Boolean)

	snapshots = relationship("CardPriceSnapshot", back_populates="identity", cascade="all, delete-orphan")
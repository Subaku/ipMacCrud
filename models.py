from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, create_engine, event, BigInteger

from time import time

Base = declarative_base()

class Device(Base):
	__tablename__ = "device"

	mac  = Column(Text, primary_key=True)
	ip   = Column(Text)
	name = Column(Text, nullable=False)
	last_updated = Column(BigInteger, onupdate=time)

	def toDict(self):
		return {
			"mac": self.mac
			,"ip": self.ip
			,"name": self.name
			,"last_updated": self.last_updated
		}

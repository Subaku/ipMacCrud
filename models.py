from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, create_engine

db = create_engine('sqlite:///ipMacCrud.db')
Base = declarative_base()


class Device(Base):
	__tablename__ = "device"

	mac  = Column(Text, primary_key=True)
	ip   = Column(Text)
	name = Column(Text, nullable=False)

	def toDict(self):
		return {
			"mac": self.mac
			,"ip": self.ip
			,"name": self.name
		}


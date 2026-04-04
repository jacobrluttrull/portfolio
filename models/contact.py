from database import Base

from sqlalchemy import Column, Integer, String, Text, DateTime, func


# Defining the Contact Model where I will include Name, Email, Message, and Phone Number(optional)
class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    subject = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    phone_number = Column(String(20))
    timestamp = Column(DateTime, server_default=func.now())


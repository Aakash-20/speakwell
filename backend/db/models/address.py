from db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


class Address(Base):
    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(255), unique=True)  
    created_at = Column(DateTime, default=datetime.now())
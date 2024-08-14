from sqlalchemy import Column, Integer, String, DateTime
from db.base_class import Base
from datetime import datetime


class Image(Base):
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    url = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.now())
from sqlalchemy import Column, Integer, String, DateTime
from db.base_class import Base
from datetime import datetime


class Image(Base):
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), unique=True, index=True)  # Added length 255
    url = Column(String(255), unique=True)  # Added length 255
    created_at = Column(DateTime, default=datetime.now())
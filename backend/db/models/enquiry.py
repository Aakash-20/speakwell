from db.base_class import Base
from sqlalchemy import Column, Integer, String, DateTime, BIGINT
from datetime import datetime

class Enquiry(Base):

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course = Column(String, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(BIGINT, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())




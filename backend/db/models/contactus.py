from db.base_class import Base
from sqlalchemy import Column, Integer, String, BIGINT

class Contact(Base):
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    phone_no = Column(BIGINT, nullable=False)
    message = Column(String, nullable=False)
    branch = Column(String, nullable=False)

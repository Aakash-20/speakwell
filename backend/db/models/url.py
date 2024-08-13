from sqlalchemy import Column, Integer, String
from db.base_class import Base


class URL(Base):

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
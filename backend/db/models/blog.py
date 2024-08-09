from datetime import datetime
from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from db.base_class import Base

class Blog(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    image = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", back_populates="blogs")
    created_at = Column(DateTime, default=datetime.now())
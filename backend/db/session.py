from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings
from typing import Generator
# from db.models.blog import Blog  
# from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL 
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SESSIONLOCAL = sessionmaker(autoflush=False, autocommit=False, bind=engine)


# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_tread":False})
# Base = declarative_base()

# Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    try:
        db = SESSIONLOCAL()
        yield db
    finally:
        db.close()

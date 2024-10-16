from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

URL = 'Ваш PostgreSQL'

engine = create_engine(URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

from backend.models import ModelsDB

Base.metadata.create_all(bind=engine)
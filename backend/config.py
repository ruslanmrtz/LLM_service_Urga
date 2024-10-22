from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

URL = 'postgresql://calls_owner:g0Z2omVMykvS@ep-calm-bar-a26gvvaw.eu-central-1.aws.neon.tech/calls?sslmode=require'

engine = create_engine(URL)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

from backend.models import ModelsDB

Base.metadata.create_all(bind=engine)
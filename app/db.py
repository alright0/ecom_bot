import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta, declarative_base

from app.config import Config as c

engine = sqlalchemy.create_engine(c.db_url, echo=False)
session = Session(bind=engine)
Base: DeclarativeMeta = declarative_base()

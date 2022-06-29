from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

from config import DATABASE_URL


engine = create_engine(DATABASE_URL)
Base = declarative_base()
session = Session(bind=engine)

class BaseSystem(object):
    def __init__(self, session: Session) -> None:
        self._session = session

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///server.db')
Base = declarative_base()


class BaseSystem(object):
    def __init__(self) -> None:
        self._session = Session(bind=engine)

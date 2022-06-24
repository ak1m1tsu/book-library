import os
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    create_engine
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


def make_db():
    engine = create_engine('sqlite:///server.db')
    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, autoincrement=True, primary_key=True)
        name = Column(String(100), index=True, unique=True, nullable=False)
        password = Column(String(1024), nullable=False)

        # relationship
        role_id = Column(Integer, ForeignKey('roles.id'))
        role = relationship('Role', lazy='subquery', backref=backref('users', lazy=True))

        def __init__(self, name: str, password: str) -> None:
            self.name = name
            self.password = password
    
    class Role(Base):
        __tablename__ = 'roles'
        id = Column(Integer, autoincrement=True, primary_key=True)
        name = Column(String(100), index=True, unique=True, nullable=False)

        def __init__(self, name) -> None:
            self.name = name

        def __repr__(self) -> str:
            return f'<Role {self.id} {self.name}>'
    
    class Book(Base):
        __tablename__ = 'books'
        id = Column(Integer, autoincrement=True, primary_key=True)
        name = Column(String(100), nullable=False)
        author = Column(String(100), nullable=False)
        pages = Column(Integer, nullable=False)

        def __init__(self, name: str, author: str, pages: int) -> None:
            self.name = name
            self.author = author
            self.pages = pages

        def __repr__(self) -> str:
            return f'<Book {self.id}>'

    if not os.path.exists('server.db'):
        with open('server.db', 'w'): pass

    try:
        Base.metadata.create_all(bind=engine)
    except Exception:
        exit(0)

if __name__ == '__main__':
    make_db()
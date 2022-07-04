import hashlib
import os

from uuid import uuid4

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    create_engine
)
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID


DATABASE_URL = os.getenv('DATABASE_URL')


def make_db():
    engine = create_engine(DATABASE_URL)
    Base = declarative_base()

    class User(Base):
        __tablename__ = 'users'
        id = Column(UUID(as_uuid=True), primary_key=True)
        name = Column(String(100), index=True, unique=True, nullable=False)
        password = Column(String(1024), nullable=False)

        # relationship
        role_id = Column(Integer, ForeignKey('roles.id'))
        role = relationship('Role', lazy='subquery')

        def __init__(self, name: str, password: str) -> None:
            self.id = uuid4()
            self.name = name
            self.password = password

    def __repr__(self) -> str:
        return f'<User {self.id} {self.name}>'
    
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

        def __init__(self, name: str, author: str, pages: int):
            self.name = name
            self.author = author
            self.pages = pages

        def __repr__(self) -> str:
            return f'<Book {self.id}>'
    try:
        admin_role = Role('admin')
        user_role = Role('user')

        password = hashlib.sha256(b'admin').hexdigest()
        admin = User('admin', password)
        admin.role = admin_role
        admin.role_id = admin_role.id

        with Session(engine) as session:
            session.begin()
            try:
                session.add(admin_role)
                session.add(user_role)
                session.add(admin)
            except:
                session.rollback()
            else:
                session.commit()
    except Exception as e:
        print('Something went wrong: ', e)
        exit(0)

if __name__ == '__main__':
    make_db()
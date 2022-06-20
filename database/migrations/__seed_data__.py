from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    create_engine
)
from sqlalchemy.orm import relationship, backref, Session
from sqlalchemy.ext.declarative import declarative_base
import hashlib


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
    try:
        admin_role = Role('admin')
        user_role = Role('user')

        password = hashlib.sha256(b'admin').hexdigest()
        admin = User('admin', password)

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
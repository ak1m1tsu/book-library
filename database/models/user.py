from database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship, backref


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
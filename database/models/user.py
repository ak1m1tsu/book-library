from uuid import uuid4
from database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


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

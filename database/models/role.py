from database import Base
from sqlalchemy import (
    Column,
    Integer,
    String
)


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(100), index=True, unique=True, nullable=False)

    def __init__(self, name) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f'<Role {self.id} {self.name}>'

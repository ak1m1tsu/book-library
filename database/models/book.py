from database import Base
from sqlalchemy import (
    Column,
    Integer,
    String
)


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

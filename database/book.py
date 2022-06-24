from exceptions import NotFoundError, AlreadyExistsError

from . import BaseSystem
from .models.book import Book


class BookSystem(BaseSystem):
    def __init__(self) -> None:
        super().__init__()

    def get_by_id(self, id: int) -> Book:
        book = self._session.query(Book) \
                            .filter_by(id=id) \
                            .first()
        
        if not book:
            raise NotFoundError(book)
        
        return book
    
    def find_by_name(self, name: str) -> list:
        books = self._session.query(Book) \
                             .filter(Book.name.ilike(name)) \
                             .all()
        
        if not books:
            raise NotFoundError(books)
        
        return books
    
    def find_by_author(self, author: str) -> list:
        books = self._session.query(Book) \
                             .filter(Book.author.ilike(author)) \
                             .all()
        
        if not books:
            raise NotFoundError(books)
        
        return books
    
    def create(self, name: str, author: str, pages: int = 1) -> int:
        book = self._session.query(Book) \
                            .filter_by(name=name, author=author, pages=pages) \
                            .first()
        
        if book:
            raise AlreadyExistsError(book)
        
        with self._session as session:
            session.begin()
            try:
                book = Book(name, author, pages)
                session.add(book)
            except Exception:
                session.rollback()
                return -1
            else:
                session.commit()
        
        return 0

    def delete(self, id: int) -> int:
        book = self._session.query(Book) \
                            .filter_by(id=id) \
                            .first()
        
        if not book:
            raise NotFoundError(book)
        
        with self._session as session:
            session.begin()
            try:
                session.delete(book)
            except Exception:
                session.rollback()
                return -1
            else:
                session.commit()
        
        return 0

book_system = BookSystem()

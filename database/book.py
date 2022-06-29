from sqlalchemy.orm import Session

from . import BaseSystem, session
from .models import Book
from exceptions import NotFoundError, AlreadyExistsError


class BookSystem(BaseSystem):
    def __init__(self, session: Session) -> None:
        super().__init__(session=session)

    def get_all(self) -> list:
        books = self._session.query(Book) \
                             .all()

        if not books:
            raise NotFoundError(books)

        return books

    def get_by_id(self, id: int) -> Book:
        book = self._session.query(Book) \
                            .filter_by(id=id) \
                            .first()

        if not book:
            raise NotFoundError(book)

        return book

    def find_by_name(self, name: str) -> list:
        books = self._session.query(Book) \
                             .filter(Book.name.ilike(f'%{name}%')) \
                             .all()

        if not books:
            raise NotFoundError(books)

        return books

    def find_by_author(self, author: str) -> list:
        books = self._session.query(Book) \
                             .filter(Book.author.ilike(f'%{author}%')) \
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

        try:
            book = Book(name, author, pages)
            self._session.add(book)
        except Exception:
            self._session.rollback()
            return -1
        else:
            self._session.commit()

        return 0

    def delete(self, id: int) -> int:
        book = self._session.query(Book) \
                            .filter_by(id = id) \
                            .first()

        if not book:
            raise NotFoundError(book)

        try:
            self._session.delete(book)
        except Exception:
            self._session.rollback()
            return -1
        else:
            self._session.commit()

        return 0


book_system = BookSystem(session)

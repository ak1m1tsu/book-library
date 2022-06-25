from exceptions import NotFoundError, AlreadyExistsError

from . import BaseSystem
from .models.user import User


class UserSystem(BaseSystem):
    def __init__(self) -> None:
        super().__init__()

    def get_by_name(self, name: str) -> User:
        user = self._session.query(User) \
                            .filter_by(name=name) \
                            .first()

        if not user:
            raise NotFoundError(user)

        return user

    def create(self, name: str, password: str) -> int:
        user = self._session.query(User) \
                            .filter_by(name=name) \
                            .first()

        if user:
            raise AlreadyExistsError(user)

        with self._session as session:
            session.begin()
            try:
                user = User(name, password)
                session.add(user)
            except Exception:
                session.rollback()
                return -1
            else:
                session.commit()

        return 0

    def delete(self, id: int) -> int:
        user = self._session.query(User) \
                            .filter_by(id=id) \
                            .first()

        if not user:
            raise NotFoundError(user)

        with self._session as session:
            session.begin()
            try:
                session.add(user)
            except Exception:
                session.rollback()
                return -1
            else:
                session.commit()

        return 0


user_system = UserSystem()

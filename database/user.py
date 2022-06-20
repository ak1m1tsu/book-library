from . import BaseSystem
from .models.user import User


class UserSystem(BaseSystem):
    def __init__(self) -> None:
        super().__init__()

    def get_by_id(self, id: int):
        user = self._session.query(User) \
                            .filter_by(id=id) \
                            .first()
        
        if not user:
            raise ValueError(f"User #{id} doesn't exists.")
        
        return user

    def get_by_name(self, name: str):
        user = self._session.query(User) \
                            .filter_by(name=name) \
                            .first()
        
        if not user:
            raise ValueError(f"User {name} doesn't exists.")
        
        return user
    
    def create(self, name: str, password: str):
        user = self._session.query(User) \
                            .filter_by(name=name) \
                            .first()
        
        if user:
            raise ValueError(f'User {name} already exists.')
        
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

    def delete(self, id: int):
        user = self._session.query(User) \
                            .filter_by(id=id) \
                            .first()
        
        if not user:
            raise ValueError(f"User #{id} doesn't exists.")
        
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

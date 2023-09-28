import logging

from sqlalchemy import create_engine, URL
from sqlalchemy import orm
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from models.user import User, DeclarativeBase
from settings import get_settings
from utils.exceptions.db_exceptions import NoSessionException

settings = get_settings('../../.env')


class DBWorker:
    def __init__(self):
        self.session: Session | None = None
        self.engine = create_engine(f'{settings.database.path}/{settings.database.users}')

    def open_session(self):
        self.session = sessionmaker(bind=self.engine)()

    def close_session(self):
        self.session.close()

    @staticmethod
    def check_session(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            if self.session is None:
                raise NoSessionException
            return func(*args, **kwargs)

        return wrapper

    @check_session
    def add_user(self, tg_id: int, location):
        user = User(tg_id=tg_id, location=';'.join(str(el) for el in location))
        self.session.add(user)
        self.session.commit()

    @check_session
    def get_user(self, user_tg_id: int) -> User | None:
        return self.session.query(User).filter_by(tg_id=user_tg_id).first()

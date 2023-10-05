from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models.user import User
from settings import get_settings
from ..logger import logger

settings = get_settings('.env')


# for tests
# settings = get_settings('../.env')


class DBWorker:
    def __init__(self, db_path=None) -> None:
        self.session: Session | None = None
        if db_path is None:
            self.engine = create_engine(f'{settings.database.path}/{settings.database.users}')
        else:
            self.engine = create_engine(db_path)

    def start_session(self) -> None:
        self.session = sessionmaker(bind=self.engine)()

    def close_session(self) -> None:
        self.session.close()

    @staticmethod
    def with_session(func):
        def wrapper(*args, **kwargs):
            self: DBWorker = args[0]
            self.start_session()
            res = func(*args, **kwargs)
            self.close_session()
            return res

        return wrapper

    @with_session
    def add_user(self, tg_id: int, location: tuple = None) -> None:
        if location is None:
            location = tuple()
        if self.get_user(tg_id):
            logger.info(f'user {tg_id} already in table, updating location to {location}')
            return self.update_user_location(tg_id, location)
        user = User(tg_id=tg_id, location=' '.join(str(el) for el in location))
        self.session.add(user)
        self.session.commit()
        logger.info(f"user {tg_id} with location {location} added to db")

    @with_session
    def update_user_location(self, tg_id: int, location: tuple) -> None:
        self.session.query(User).filter_by(tg_id=tg_id).update({User.location: ' '.join((str(el) for el in location))})
        self.session.commit()
        logger.info(f"location {location} for user {tg_id} added")

    @with_session
    def get_user(self, user_tg_id: int) -> User | None:
        return self.session.query(User).filter_by(tg_id=user_tg_id).first()

    @with_session
    def remove_user(self, user_tg_id: int) -> None:
        self.session.query(User).filter_by(tg_id=user_tg_id).delete()
        self.session.commit()

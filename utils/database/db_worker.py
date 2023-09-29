from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from .models.user import User
from settings import get_settings
from utils.exceptions.db_exceptions import NoSessionException

settings = get_settings('.env')


class DBWorker:
    def __init__(self):
        self.session: Session | None = None
        self.engine = create_engine(f'{settings.database.path}/{settings.database.users}')

    def start_session(self):
        self.session = sessionmaker(bind=self.engine)()

    def close_session(self):
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
    def add_user(self, tg_id: int, location: tuple = None):
        if location is None:
            location = tuple()
        print(location)
        user = User(tg_id=tg_id, location=' '.join(str(el) for el in location))
        self.session.add(user)
        self.session.commit()

    @with_session
    def update_user_location(self, tg_id: int, location: tuple):
        self.session.query(User).filter_by(tg_id=tg_id).update({User.location: ' '.join((str(el) for el in location))})
        self.session.commit()

    @with_session
    def get_user(self, user_tg_id: int) -> User | None:
        return self.session.query(User).filter_by(tg_id=user_tg_id).first()

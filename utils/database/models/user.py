from sqlalchemy import BigInteger, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DeclarativeBase = declarative_base()


class User(DeclarativeBase):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tg_id = Column(BigInteger, index=True)
    location = Column(String)

    def __repr__(self) -> str:
        return f'User(id={self.id}, tg_id={self.tg_id}, location={self.location})'


def wipe_user_table():
    from settings import get_settings

    settings = get_settings('../../../.env')

    engine = create_engine(f'{settings.database.path}/{settings.database.users}')
    session_class = sessionmaker(bind=engine)
    db_session = session_class()

    DeclarativeBase.metadata.drop_all(engine)
    DeclarativeBase.metadata.create_all(engine)
    db_session.commit()
    db_session.close()
    print('users wiped!')


if __name__ == '__main__':
    wipe_user_table()

from os import getenv
from dotenv import load_dotenv
from dataclasses import dataclass


@dataclass
class Bots:
    bot_token: str
    admin_id: int


@dataclass
class DataBase:
    path: str
    users: str = 'users'


@dataclass
class Weather:
    api_key: str
    server: str = 'openweathermap.org'


@dataclass
class Geocoder:
    api_key: str
    params: dict
    url: str = 'https://geocode-maps.yandex.ru/1.x'


@dataclass
class Settings:
    bots: Bots
    database: DataBase
    weather: Weather
    geocoder: Geocoder


def get_settings(path: str):
    load_dotenv(path)

    return Settings(
        bots=Bots(
            bot_token=getenv('BOT_TOKEN'),
            admin_id=int(getenv('ADMIN_ID')),
        ),
        database=DataBase(
            path=getenv('DB_PATH')
        ),
        weather=Weather(
            api_key=getenv('OWM_API_KEY')
        ),
        geocoder=Geocoder(
            api_key=getenv('YANDEX_GEOCODER_API_KEY'),
            params={
                'format': 'json'
            }
        )
    )

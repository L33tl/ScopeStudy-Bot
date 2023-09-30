import socket
from collections import namedtuple

from pyowm import OWM
from pyowm.utils.config import get_default_config

from settings import get_settings
from utils.exceptions.geocoder_exceptions import GeocoderHttpException, GeocoderToponymNotFoundException
from bot.misc.tguser import Location

import requests

settings = get_settings('.env')

weather_server = settings.weather.server
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM(settings.weather.api_key, config_dict)
weather_mgr = owm.weather_manager()


class WeatherManager:
    @staticmethod
    def get_location_by_toponym(toponym: str) -> dict:
        response = requests.get(
            f'{settings.geocoder.url}?apikey={settings.geocoder.api_key}',
            params={'geocode': toponym, **settings.geocoder.params}
        )

        if response.status_code != 200:
            raise GeocoderHttpException(
                f'{response.status_code}'
                'Non-200 response from yandex geocoder'
            )
        return response.json()['response']

    @classmethod
    def coordinates(cls, toponym: str) -> namedtuple:
        """Returns a tuple of coordinates (longitude, latitude) for toponym

        Raises 'GeocoderToponymNotFoundException if nothing found.

        """
        data = cls.get_location_by_toponym(toponym)['GeoObjectCollection']['featureMember']

        if not data:
            raise GeocoderToponymNotFoundException(f'{toponym} not found')

        location = data[0]['GeoObject']['Point']['pos'].split()[::-1]
        return cls.from_tuple(location)

    @staticmethod
    def with_connection(func):
        def wrapper(*args, **kwargs):
            socket.create_connection(weather_server, 80)
            return func(*args, **kwargs)

        return wrapper

    @staticmethod
    def get_weather(mode: str | int, location: Location):
        match mode:
            case 1 | 'today':
                return weather_mgr.weather_at_coords(lat=location.lat, lon=location.lon)
            case 2 | 'tomorrow':
                return weather_mgr.one_call(lat=location.lat, lon=location.lon).forecast_daily[1]
            case 5 | 'five':
                return weather_mgr.one_call(lat=location.lat, lon=location.lon).forecast_daily
            case 7 | 'week':
                return weather_mgr.one_call(lat=location.lat, lon=location.lon).forecast_daily

    @staticmethod
    def from_tuple(location: tuple[float | str, float | str]) -> Location:
        print(location)
        return Location(lat=float(location[0]), lon=float(location[1]))

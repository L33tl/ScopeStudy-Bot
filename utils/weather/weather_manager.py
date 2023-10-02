import datetime
import socket
from collections import namedtuple

from pyowm import OWM
from pyowm.utils.config import get_default_config

from settings import get_settings
from utils.exceptions.geocoder_exceptions import GeocoderHttpException, GeocoderToponymNotFoundException
from bot.misc.classes import Location, WeatherDay, parse_weather

import requests


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

    @classmethod
    def get_weather(cls, mode: str | int, location: Location):
        match mode:
            case 1 | 'today':
                return weather_mgr.weather_at_coords(lat=location.lat, lon=location.lon).to_dict().get('weather')
            case 2 | 'tomorrow':
                return weather_mgr.one_call(lat=location.lat, lon=location.lon).forecast_hourly[24:]
            case 5 | 'five':
                return weather_mgr.one_call(lat=location.lat, lon=location.lon).forecast_daily
            case 7 | 'week':
                return weather_mgr.one_call(lat=location.lat, lon=location.lon).forecast_hourly

    @classmethod
    def get_beauty_weather(cls, mode, location):
        return cls.beautify_weather(cls.get_weather(mode, location))

    @staticmethod
    def from_tuple(location: tuple[float | str, float | str]) -> Location:
        return Location(lat=float(location[0]), lon=float(location[1]))

    @classmethod
    def beautify_weather(cls, weather: dict) -> str:
        # •{settings.weather.img_url}{weather.weather_icon_name}.png

        weather: WeatherDay = parse_weather(weather)
        print(f'<img src="{settings.weather.img_url}{weather.weather_icon_name}.png">')
        result = f"""Погода на 📆{weather.reference_time.strftime('%d.%m.%Y')}    🕰{weather.reference_time.strftime('%H:%M')}"""
        if weather.temperature:
            result += f"""
            \n🌡 Температура
            \t•Текущая  {cls.to_celsius_from_kelvin(weather.temperature.temp)}°C
            \t•Ощущается как  {cls.to_celsius_from_kelvin(weather.temperature.feels_like)}°C
            \t•Минимальная  {cls.to_celsius_from_kelvin(weather.temperature.temp_min)}°C
            \t•Максимальная  {cls.to_celsius_from_kelvin(weather.temperature.temp_max)}°C
            """
        if weather.wind:
            result += f"""\n🌬️ Ветер
            \t 👨‍🦼Скорость - {weather.wind.speed} м/c
            \t 🧭Направление - {weather.wind.deg}°
            \t 💨Порывы - {weather.wind.gust or 0} м/c
            """
        if weather.rain:
            many = weather.rain.h3 is not None
            result += f"""\n🌧️ Дождь
            \t За последни{'ие' if many else 'й'} {'3' if many else ''} час{'а' if many else ''} выпало {weather.rain.h3 if many else weather.rain.h1} мм осадков"""
        if weather.snow:
            many = weather.snow.h3 is not None
            result += f"""\n☃️ Снег
            \t За последни{'ие' if many else 'й'} {'3' if many else ''} час{'а' if many else ''} выпало {weather.snow.h3 if many else weather.snow.h1} мм осадков"""
        print(weather)

        return result

    @staticmethod
    def to_celsius_from_kelvin(kelvin):
        return round(kelvin - 273.15, 1)


if __name__ != '__main__':
    settings = get_settings('.env')
    weather_server = settings.weather.server
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM(settings.weather.api_key, config_dict)
    weather_mgr = owm.weather_manager()

if __name__ == '__main__':
    settings = get_settings('../../.env')

    weather_server = settings.weather.server
    config_dict = get_default_config()
    config_dict['language'] = 'ru'
    owm = OWM(settings.weather.api_key, config_dict)
    weather_mgr = owm.weather_manager()

    loc = Location(26.274030, 70.269901)
    loc = Location(0, 0)
    import json

    js = json.dumps(WeatherManager.get_weather(5, loc)[0].to_dict(), indent=3)
    print(js)
    # print('\n'.join(el for el in ((WeatherManager.get_weather(5, loc)))[-1].to_dict()))

from collections import namedtuple

from pyowm import OWM
from pyowm.utils.config import get_default_config

from settings import get_settings
from utils.exceptions.geocoder_exceptions import GeocoderHttpException, GeocoderToponymNotFoundException
from bot.misc.classes import Location, Weather, parse_weather

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
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={location.lat}&lon={location.lon}&exclude=current,minutely,hourly,alerts&lang=ru&appid={settings.weather.api_key}"



        daily_data = requests.get(url)
        if daily_data.status_code == 200:
            daily_data = daily_data.json()['daily']
        else:
            print('error')

        match mode:
            case 1 | 'today':
                return daily_data[0]
            case 2 | 'tomorrow':
                return daily_data[1]

    @classmethod
    def get_beauty_weather_day(cls, mode, location):
        return cls.beautify_weather_day(cls.get_weather(mode, location))

    @classmethod
    def beautify_weather_day(cls, weather: dict) -> str:
        # •{settings.weather.img_url}{weather.weather_icon_name}.png
        weather: Weather = parse_weather(weather)
        print(f'<img src="{settings.weather.img_url}{weather.weather_icon_name}.png">')
        result = f"""Погода на 📆 {weather.reference_time.strftime('%d.%m.%Y')}
        \n🗣️ {weather.description}\n\tОбщее облачное покрытие неба - {weather.clouds}%
        """
        if weather.temperature:
            result += f"""
            \n🌡 Температура
              • Максимальная  {cls.to_celsius_from_kelvin(weather.temperature.max)}°C
              • Минимальная  {cls.to_celsius_from_kelvin(weather.temperature.min)}°C

              🌻 Утро
            \t• Средняя  {cls.to_celsius_from_kelvin(weather.temperature.morn)}°C
            \t• Ощущается как  {cls.to_celsius_from_kelvin(weather.temperature.feels_like_morn)}°C
            
              ☀️ День
            \t• Средняя  {cls.to_celsius_from_kelvin(weather.temperature.day)}°C
            \t• Ощущается как  {cls.to_celsius_from_kelvin(weather.temperature.feels_like_day)}°C

              🌇 Вечер
            \t• Средняя  {cls.to_celsius_from_kelvin(weather.temperature.eve)}°C
            \t• Ощущается как  {cls.to_celsius_from_kelvin(weather.temperature.feels_like_eve)}°C

              🌙 Ночь
            \t• Средняя  {cls.to_celsius_from_kelvin(weather.temperature.night)}°C
            \t• Ощущается как  {cls.to_celsius_from_kelvin(weather.temperature.feels_like_night)}°C
            """
        if weather.wind:
            result += f"""\n🌬️ Ветер
            \t 👨‍🦼Скорость - {weather.wind.speed} м/c
            \t 🧭Направление - {weather.wind.deg}°
            \t 💨Порывы - {weather.wind.gust or 0} м/c
            """
        if weather.rain:
            result += f"""\n🌧️ Дождь
            \tВероятность -  {round(weather.precipitation_probability * 100)}%
            \tОжидается {weather.rain} мм осадков"""
        if weather.snow:
            result += f"""\n☃️ Снег
            \tОжидается {weather.snow} мм осадков"""
        if weather.pressure:
            result += f'\n\n⏲️ Давление - {cls.to_mm_from_hpa(weather.pressure)} мм рт. ст.'

        result += '\n\nУдачного Дня!💪'

        print(weather)

        return result

    @staticmethod
    def from_tuple(location: tuple[float | str, float | str]) -> Location:
        return Location(lat=float(location[0]), lon=float(location[1]))

    @staticmethod
    def to_celsius_from_kelvin(kelvin):
        return round(kelvin - 273.15, 1)

    @staticmethod
    def to_mm_from_hpa(hpa):
        return round(hpa * 0.750064, 1)


if __name__ != '__main__':
    settings = get_settings('.env')
    weather_server = settings.weather.server
    config_dict = get_default_config()
    # config_dict['language'] = 'ru'
    owm = OWM(settings.weather.api_key, config_dict)
    weather_mgr = owm.weather_manager()

if __name__ == '__main__':
    settings = get_settings('../../.env')

    weather_server = settings.weather.server
    config_dict = get_default_config()
    # config_dict['language'] = 'ru'
    owm = OWM(settings.weather.api_key, config_dict)
    weather_mgr = owm.weather_manager()

    loc = Location(lat=59.924176, lon=30.455071)

    # print('\n'.join(WeatherManager.get_weather(2, loc)['weather']))
    print(WeatherManager.get_weather(2, loc)['weather'])

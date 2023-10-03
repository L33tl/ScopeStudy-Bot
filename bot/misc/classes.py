from dataclasses import dataclass
from collections import namedtuple
from datetime import datetime

Location = namedtuple('Location', 'lat, lon')


@dataclass
class TgUser:
    tg_id: int
    location: Location = None


@dataclass
class Wind:
    speed: int
    deg: int
    gust: int


@dataclass
class Temperature:
    max: int
    min: int
    morn: int
    feels_like_morn: int
    day: int
    feels_like_day: int
    eve: int
    feels_like_eve: int
    night: int
    feels_like_night: int


@dataclass
class Weather:
    reference_time: int
    sunset_time: int
    sunrise_time: int
    clouds: int
    rain: float
    snow: float
    wind: Wind
    humidity: int
    pressure: int
    temperature: Temperature
    status: str
    detailed_status: str
    weather_code: int
    weather_icon_name: str
    description: str
    dewpoint: int
    humidex: None
    heat_index: None
    utc_offset: int
    uvi: int
    precipitation_probability: int


def parse_weather(weather: dict) -> Weather:
    wind, temperature = None, None
    if weather.get('wind_speed'):
        wind = Wind(
            speed=weather.get('wind_speed'),
            deg=weather.get('wind_deg'),
            gust=weather.get('wind_gust')
        )
    if weather.get('temp'):
        temperature_d: dict = weather.get('temp')
        feels_like: dict = weather.get('feels_like')
        temperature = Temperature(
            day=temperature_d.get('day'),
            min=temperature_d.get('min'),
            max=temperature_d.get('max'),
            night=temperature_d.get('night'),
            eve=temperature_d.get('eve'),
            morn=temperature_d.get('morn'),
            feels_like_day=feels_like.get('day'),
            feels_like_night=feels_like.get('night'),
            feels_like_morn=feels_like.get('morn'),
            feels_like_eve=feels_like.get('eve'),
        )
    return Weather(
        reference_time=datetime.fromtimestamp(weather.get('dt')),
        sunrise_time=datetime.fromtimestamp(weather.get('sunrise')),
        sunset_time=datetime.fromtimestamp(weather.get('sunset')),
        clouds=weather.get('clouds'),
        rain=weather.get('rain'),
        snow=weather.get('snow'),
        wind=wind,
        description=weather.get('weather')[0].get('description'),
        humidity=weather.get('humidity'),
        pressure=weather.get('pressure'),
        temperature=temperature,
        status=weather.get('status'),
        detailed_status=weather.get('detailed_status'),
        weather_code=weather.get('weather_code'),
        weather_icon_name=weather.get('weather_icon_name'),
        dewpoint=weather.get('dewpoint'),
        humidex=weather.get('humidex'),
        heat_index=weather.get('heat_index'),
        utc_offset=datetime.fromtimestamp(weather.get('utc_offset') or 0),
        uvi=weather.get('uvi'),
        precipitation_probability=weather.get('pop')
    )

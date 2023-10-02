from dataclasses import dataclass
from collections import namedtuple
from datetime import datetime

Location = namedtuple('Location', 'lat, lon')


@dataclass
class TgUser:
    tg_id: int
    location: Location = None


@dataclass
class Rain:
    h1: int
    h3: int


@dataclass
class Snow:
    h1: int
    h3: int


@dataclass
class Wind:
    speed: int
    deg: int
    gust: int


@dataclass
class Pressure:
    value: int
    unit: str


@dataclass
class Temperature:
    temp: int
    temp_max: int
    temp_min: int
    feels_like: int


@dataclass
class WeatherDay:
    reference_time: int
    sunset_time: int
    sunrise_time: int
    clouds: int
    rain: Rain
    snow: Snow
    wind: Wind
    humidity: int
    pressure: Pressure
    temperature: Temperature
    status: str
    detailed_status: str
    weather_code: int
    weather_icon_name: str
    visibility_distance: int
    dewpoint: None
    humidex: None
    heat_index: None
    utc_offset: int
    uvi: None
    precipitation_probability: None


def parse_weather(weather: dict) -> WeatherDay:
    rain, snow, wind, pressure, temperature = (None,) * 5
    if weather.get('rain'):
        rain_d = weather.get('rain')
        rain = Rain(
            h1=rain_d.get('1h'),
            h3=rain_d.get('3h')
        )
    if weather.get('snow'):
        snow_d = weather.get('snow')
        snow = Snow(
            h1=snow_d.get('1h'),
            h3=snow_d.get('3h')
        )
    if weather.get('wind'):
        wind_d = weather.get('wind')
        wind = Wind(
            speed=wind_d.get('speed'),
            deg=wind_d.get('deg'),
            gust=wind_d.get('gust')
        )
    if weather.get('pressure'):
        pressure_d = weather.get('pressure')
        pressure = Pressure(
            value=pressure_d.get('value'),
            unit=pressure_d.get('unit')
        )
    if weather.get('temperature'):
        temperature_d: dict = weather.get('temperature')
        temperature = Temperature(
            temp=temperature_d.get('temp'),
            temp_min=temperature_d.get('temp_min'),
            temp_max=temperature_d.get('temp_max'),
            feels_like=temperature_d.get('feels_like')
        )
    return WeatherDay(
        reference_time=datetime.fromtimestamp(weather.get('reference_time')),
        sunset_time=datetime.fromtimestamp(weather.get('sunset_time')),
        sunrise_time=datetime.fromtimestamp(weather.get('sunrise_time')),
        clouds=weather.get('clouds'),
        rain=rain,
        snow=snow,
        wind=wind,
        humidity=weather.get('humidity'),
        pressure=pressure,
        temperature=temperature,
        status=weather.get('status'),
        detailed_status=weather.get('detailed_status'),
        weather_code=weather.get('weather_code'),
        weather_icon_name=weather.get('weather_icon_name'),
        visibility_distance=weather.get('visibility_distance'),
        dewpoint=weather.get('dewpoint'),
        humidex=weather.get('humidex'),
        heat_index=weather.get('heat_index'),
        utc_offset=datetime.fromtimestamp(weather.get('utc_offset') or 0),
        uvi=weather.get('uvi'),
        precipitation_probability=weather.get('precipitation_probability')
    )

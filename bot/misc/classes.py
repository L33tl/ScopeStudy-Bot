from dataclasses import dataclass
from collections import namedtuple

Location = namedtuple('Location', 'lat, lon')


@dataclass
class TgUser:
    tg_id: int
    location: Location = None


@dataclass
class Rain:
    pass


@dataclass
class Snow:
    pass


@dataclass
class Wind:
    pass


@dataclass
class Pressure:
    pass


@dataclass
class Temperature:
    pass


@dataclass
class Weather:
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

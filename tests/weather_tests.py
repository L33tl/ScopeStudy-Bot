from pyowm import OWM
from pyowm.utils.config import get_default_config

from bot.misc.classes import Location
from settings import get_settings
from utils.weather.weather_manager import WeatherManager

from utils.exceptions.geocoder_exceptions import GeocoderToponymNotFoundException

import unittest


class TestWeatherManager(unittest.TestCase):
    def setUp(self) -> None:
        self.location = Location(lat=59.955783, lon=30.297927)

    def test_get_location_by_toponym(self):
        self.assertEqual(WeatherManager.get_location_by_toponym('aaaaaaaaaaaaaaa'), [])
        self.assertIsNotNone(WeatherManager.get_location_by_toponym('Исаакиевский Собор'))

    def test_coordinates(self):
        self.assertIsInstance(WeatherManager.coordinates('Большая конюшенная 25'), Location)
        with self.assertRaises(GeocoderToponymNotFoundException):
            WeatherManager.coordinates('aaaaaaaaaaaaaaaaaaaa')

    def test_get_weather(self):
        self.assertIsInstance(WeatherManager.get_weather(1, self.location), dict)
        self.assertIsInstance(WeatherManager.get_weather('today', self.location), dict)
        self.assertIsInstance(WeatherManager.get_weather(2, self.location), dict)
        self.assertIsNone(WeatherManager.get_weather(32132, self.location))

    def test_beautify_weather_day(self):
        self.assertIsInstance(WeatherManager.beautify_weather_day(WeatherManager.get_weather(1, self.location)), str)

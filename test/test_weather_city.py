import unittest
from weather_server import get_city_weather

class TestWeathercity(unittest.TestCase):
    def test_get_weather(self):
        result=get_city_weather('tehran').get('status')
        self.assertEqual(result,200)

if __name__ == '__main__':
    unittest.main()
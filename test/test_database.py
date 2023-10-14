import unittest
from database import *
from main import get_result
import datetime
from decimal import Decimal

class TestDatabase(unittest.TestCase):
    def test_save_request_data(self):
        WeatherDatabase.save_request_data('chalus','2024-1-1 20:25:26')
        query='SELECT * FROM request ORDER BY request_id DESC LIMIT 1;'
        result=get_result(query)
        tim=datetime.datetime.strptime('2024-1-1 20:25:26','%Y-%m-%d %H:%M:%S')
        self.assertEqual(result,[(20,'chalus',tim)])
    
    def test_save_response_data(self):
        tim=datetime.datetime.strptime('2024-1-1 20:25:26','%Y-%m-%d %H:%M:%S')
        data={'Temperature':'18.17','Feels like': '17.54','Last update': tim,'status': 200} 
        WeatherDatabase.save_response_data('paris',data)
        query='SELECT * FROM response ORDER BY response_id DESC LIMIT 1;'
        result=get_result(query)
        self.assertEqual(result,[(22,'200','paris',Decimal('18.1'),Decimal('17.5'),tim,22)])

    def test_request_count(self):
        result=WeatherDatabase.get_request_count()

        """ We can check the database and find out how many we request count """

        query=f"SELECT count(*) FROM response;"
        request_count=int(get_result(query)[0][0])
        self.assertEqual(result,request_count)

    def test_get_succesful_request_count(self):
        result=WeatherDatabase.get_successful_request_count()
        """ We can check the database and find out how many we request count """
        query=f"SELECT count(*) FROM response WHERE status = '200';"
        response_count=int(get_result(query)[0][0])
        self.assertEqual(result,response_count)

    def test_last_hour(self):
        result=WeatherDatabase.last_hour()
        """ We can check the database and find out how many we request count """
        query=f"SELECT * FROM request WHERE cast(date_of_request AS time) > (current_time-'01:00:00') AND DATE(NOW()) = date(date_of_request);;"
        last_hour_count=get_result(query)
        for i,item in enumerate(last_hour_count):
            item=list(item)
            item[2] = str(item[2])
            result[i]=tuple(item)
        
        self.assertEqual(result,last_hour_count)

    def test_get_city(self):
        result=WeatherDatabase.get_city()
        """ We can check the database and find out how many we request count """
        query=f"SELECT city,count(*) FROM request GROUP BY city;"
        get_city_count=get_result(query)
        self.assertEqual(result,get_city_count)


if __name__ == '__main__':
    unittest.main()
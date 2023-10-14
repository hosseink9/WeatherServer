from typing import List, Tuple
from main import get_result,insert,connect


class WeatherDatabase:
    @staticmethod
    def save_request_data(city_name: str, request_time: str) -> None:
        query=f"INSERT INTO request (city,date_of_request) VALUES ('{city_name}','{request_time}');"
        insert(query)
        
    @staticmethod
    def save_response_data(city_name: str, response_data: dict) -> None:
        data=response_data
        data1=data.get('Temperature','')
        data2=data.get('Feels like','')
        data3=data.get('Last update','')
        data4=data.get('status')
        if data4 == 200:
            query=f"INSERT INTO response (status,city,temperature,feels_like,last_updated_time) VALUES ('{data4}','{city_name}','{data1[0:4]}','{data2[0:4]}','{data3}');"  
            
        else:
            query=f"INSERT INTO response (status,city) VALUES ('{data4}','{city_name}');"   
        insert(query)
    
    @staticmethod
    def get_request_count() -> int:
        
        query=f"SELECT count(*) FROM response;"
        return int(get_result(query)[0][0])

    @staticmethod
    def get_successful_request_count() -> int:

        query=f"SELECT count(*) FROM response WHERE status = '200';"
        return int(get_result(query)[0][0])

    
    @staticmethod
    def last_hour() -> List[Tuple]:
        query=f"SELECT * FROM request WHERE cast(date_of_request AS time) > (current_time-'01:00:00') AND DATE(NOW()) = date(date_of_request);;"
        result=get_result(query)
        for i,item in enumerate(result):
            item=list(item)
            item[2] = str(item[2])
            result[i]=tuple(item)
            
        return result
        
    @staticmethod
    def get_city() -> List[Tuple]:
        query=f"SELECT city,count(*) FROM request GROUP BY city;"
        return get_result(query)
    
    @staticmethod
    def check_cache(city) -> List[Tuple]:
        query=F"SELECT * FROM response WHERE cast(last_updated_time AS time) > (current_time-'00:10:00') AND DATE(NOW()) = date(last_updated_time) AND city = '{city}' ORDER BY last_updated_time DESC LIMIT 1;"
        return get_result(query)
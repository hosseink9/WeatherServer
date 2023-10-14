import requests
import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from database import *
import logging
from requests import exceptions as req_exception

logger = logging.getLogger('__main__')
file_formatter = logging.Formatter(fmt='%(name)s - %(funcName)s - %(created)f - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(filename='server_log.log', mode='a')
file_handler.setFormatter(fmt=file_formatter)
stream_handler = logging.StreamHandler()
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
file_handler.setLevel(10) 
stream_handler.setLevel(20)

HOST='192.168.1.13'
PORT = 8000


def get_city_weather(city: str) -> dict:
    url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=69eb8df405626f554627f041b72f1332"
    response = requests.get(url,timeout=1)
    print(response.status_code)
    try:
        t=str(datetime.datetime.now())
        data=response.json()
        if data.get('main'):
            data2=data["main"]
            data3=data2["temp"]
            data4=data2["feels_like"]
            temp=float(data3)-273.15
            temp=f'{round(temp,2)}°C'
            feels_like=float(data4)-273.15
            feels_like=f'{round(feels_like,2)}°C'
            return {'Temperature':temp,'Feels like': feels_like,'Last update': t,'status': response.status_code} 
        else:      
            logger.error('Error retrieving weather data: No matching location found.')       
            return {'error': 'Error retrieving weather data: No matching location found.','status': response.status_code,'Last update':t}
    except req_exception.ConnectionError:
        logger.warning('Connection lost!')
    except req_exception.JSONDecodeError:
        logger.warning('Invalid URL!')

request_type={'Request count':WeatherDatabase.get_request_count,
              'Successful request count':WeatherDatabase.get_successful_request_count
              ,'Last hour requests': WeatherDatabase.last_hour
              ,'City request counts': WeatherDatabase.get_city}   
lst=[]
class WeatherServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(lst).encode('utf-8'))

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        post_body1=json.loads(post_body)
        print(post_body1.keys())
        print(list(post_body1.items()))
        if list(post_body1.keys())[0]=='city':
            self.get_city_data(post_body1) 
        else:
            self.db_result(list(post_body1.keys())[0])

    def get_city_data(self,post_body1):
        city=post_body1.get('city')
        t=datetime.datetime.now()
        t=str(datetime.datetime.strftime(t,'%Y-%m-%d %H:%M:%S'))
        WeatherDatabase.save_request_data(city,t)
        result1=WeatherDatabase.check_cache(city)
        if result1:
            print('database')
            result = self.from_cache(result1)
        else:    
            print('sever')
            result=get_city_weather(city)

        lst.insert(0,result)
        WeatherDatabase.save_response_data(city,result)
        print(result)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write('finish'.encode('utf-8'))
        
    def db_result(self,key):
        result= request_type.get(key)()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

    def from_cache(self,city):
        t=str(datetime.datetime.now())
        feels_like=f'{float(city[0][4])}°C' #database fourth element is feels like 
        temp=f'{float(city[0][3])}°C' #database third element is temperature 
        result_response={'Temperature':temp,'Feels like': feels_like ,'Last update': t,'status': int(city[0][1])}
        return result_response
    
def start_server():
    try:
        with HTTPServer((HOST,PORT),WeatherServer) as server:
            print('on')
            server.serve_forever()
    except KeyboardInterrupt as error:
        logger.error(f'Server is off {error}')
        server.server_close()
        # print('Server is off',error)
                
if __name__ == '__main__':
    start_server()



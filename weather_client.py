import requests

def client():
    while True:
        print('\n1)See weather\n2)See database\n3)Exit')
        select=input("\nSelect your option: ")
        if select == '1':
            weather=input('Enter city for weather: ')
            response=requests.post('http://192.168.1.13:8000/',
                        json={'city':weather})
            response = requests.get('http://192.168.1.13:8000/')
            result=response.json()
            if result[0].get('status')==200:
                print(f"Temperature: {result[0].get('Temperature')}\nFeels like: {result[0].get('Feels like')}\nLast update: {result[0].get('Last update')}")
            else:
                print(result[0].get('error'))
        if select == '2':
            while True:
                print('\n1)Request count\n2)Successful request count\n3)Last hour requests\n4)City request count\n5)Back')
                select=input("\nSelect your option: ")
                if select == '1':
                    response1=requests.post('http://192.168.1.13:8000/',
                            json={'Request count': ''})
                    print(f"\nRequest count: {response1.text}")

                if select == '2':
                    response2=requests.post('http://192.168.1.13:8000/',
                            json={'Successful request count': ''})
                    print(f"\nSuccessful request count: {response2.text}")
                    
                if select == '3':
                    response3=requests.post('http://192.168.1.13:8000/',
                            json={'Last hour requests': ''})
                    print(f"\nLast hour requests: {response3.text}")

                if select == '4':
                    response4=requests.post('http://192.168.1.13:8000/',
                            json={'City request counts': ''})
                    print(f"\nCity request counts: {response4.text}")
                
                if select == '5':
                    break

                # print(f"Request count: {response1.text}\nSuccessful request count: {response2.text}\nLast hour requests: {response3.text}\nCity request counts: {response4.text}")
                
        if select == '3':
            print('Good bye!!')
            exit()
        
        else: 
            client()
client()
            
        
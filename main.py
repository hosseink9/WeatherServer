import psycopg2
from config import config

# connection=psycopg2.connect(
#     host='localhost',port='5432',
#     database='master',user='hosseink9')


def connect():
    connection=None
    
    try:
        params=config()
        print('Connecting to the postgreSQL database...')
        connection=psycopg2.connect(**params)
        
        #create a cursor
        crsr=connection.cursor()
        print('PstgreSQL database version: ')
        crsr.execute('SELECT version()')
        db_version = crsr.fetchone()
        print(db_version)
        
        crsr.execute(
            """CREATE TABLE response(
                response_id serial PRIMARY KEY,
                status VARCHAR(20) NOT NULL,
                city VARCHAR(50),
                temperature NUMERIC,
                feels_like NUMERIC,
                last_updated_time TIMESTAMP,
                request_id serial);""")
        
        crsr.execute(
            """CREATE TABLE request(
                request_id serial PRIMARY KEY,
                city VARCHAR(50) NOT NULL,
                date_of_request TIMESTAMP);""")
        
        # crsr.execute(enter_request)
        
        connection.commit()
        # crsr.execute("SELECT * FROM useres;")
        # a=crsr.fetchall()
        # print('\n',a,'\n')
        # print('[INFO] Table created succesfully')
        crsr.close()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if connection is not None:
            connection.close()
            print('Database connection terminal')
            

def insert(query):
    connection=None
    print(query)
    try:
        params=config()
        connection=psycopg2.connect(**params)
        
        crsr=connection.cursor()
        
        crsr.execute(query)
        print('process done succesfuly')
        connection.commit()
        crsr.close()
        
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if connection is not None:
            connection.close()
            # print('Database connection terminal')
    
def get_result(query):
    connection=None
    try:
        params=config()
        connection=psycopg2.connect(**params)
        
        crsr=connection.cursor()
        
        crsr.execute(query)
        a=crsr.fetchall()
        connection.commit()
        crsr.close()
        return a
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if connection is not None:
            connection.close()
            # print('Database connection terminal')
    

if __name__ == '__main__':
    connect()
    
    
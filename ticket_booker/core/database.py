from psycopg2 import pool
from .config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_USER
from fastapi.exceptions import HTTPException
print(POSTGRES_HOST)
class DBConnection:            
    
    def __init__(self):
        try:
            self.connections = pool.SimpleConnectionPool(
                minconn = 2, maxconn = 15,
                dbname = POSTGRES_DB, user = POSTGRES_USER, password = POSTGRES_PASSWORD,
                host = "localhost", port = '5432'
            )
        except Exception as e:
            print(e)
            self.connections = None

    def get_conn(self):
        if self.connections:
            return self.connections.getconn()
        return None
    
    def release_conn(self, connection):
        if self.connections and connection:
            self.connections.putconn(connection)
        return 

db_instance = DBConnection()

def db_connector():
    try:
        connection = db_instance.get_conn()
        if not connection:
            raise HTTPException(500, detail='server exception occured')
        yield connection
    except Exception as e:
        raise HTTPException(500, detail='server exception occured')
        print(e)
    else:
        db_instance.release_conn(connection)
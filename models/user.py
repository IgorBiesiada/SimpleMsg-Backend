import bcrypt
from psycopg2 import connect 
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

USER = os.getenv("USER")
HOST = os.getenv('HOST')
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

@contextmanager
def save_data_to_db():
    try:
        ctx = connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
        ctx.autocommit = True
        cursor = ctx.cursor()
        yield cursor
    
    except Exception as e:
        print(f"Błąd {e}")
    
    finally:
        cursor.close()
        ctx.close()

class User:
    def __init__(self, username, password):
        self._id = -1
        self.username = username
        self._hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    @property
    def id(self):
        return self._id
    
    @property
    def hashed_password(self):
        return self._hashed_password.decode('utf-8')
    
    def set_new_pass(self, old_password: str, new_password: str) -> str:
        b_old_password = old_password.encode('utf-8')
        b_new_password = new_password.encode('utf-8')
        
        if bcrypt.checkpw(b_old_password, self._hashed_password):
            self._hashed_password = bcrypt.hashpw(b_new_password, bcrypt.gensalt())
            return self._hashed_password.decode('utf-8')
        else:
            print("Hasło nie pasuje")

    def save_to_db(self):
        
        with save_data_to_db() as cursor:
        
            sql = "INSERT INTO users (username, hashed_password) VALUES (%s, %s)"
            data = (self.username, self._hashed_password.decode('utf-8'))
            cursor.execute(sql, data)

u = User("marek", "siema1234")
u.save_to_db()
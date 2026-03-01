import bcrypt
from psycopg2 import connect, errors, DatabaseError 
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
    def __init__(self, username, password, first_name, last_name):
        self._id = -1
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
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

    def _insert(self):
        
        try: 
            with save_data_to_db() as cursor:
                sql = "INSERT INTO users (username, hashed_password, first_name, last_name) VALUES (%s, %s, %s, %s);"
                data = (self.username, self._hashed_password.decode('utf-8'), self.first_name, self.last_name)
                cursor.execute(sql, data)
        except errors.UniqueViolation:
            print("Uzytkownik o takiej nazwie juz istnieje")
    
    def _update(self, **kwargs):
        data_to_update = ("username", "first_name", "last_name", "password")
        
        for key, value in kwargs.items():
            if key not in data_to_update:
                raise ValueError
        
            if key == "password":
                b_password = value.encode('utf-8')
                hashed_password = bcrypt.hashpw(b_password, bcrypt.gensalt())
                setattr(self, "_hashed_password", hashed_password)
            
            elif key in data_to_update:
                setattr(self, key, value)
        
        try:
            with save_data_to_db() as cursor:
                sql = "UPDATE users SET username=%s, first_name=%s, last_name=%s, hashed_password=%s;"
                data = (self.username, self.first_name, self.last_name, self._hashed_password.decode('utf-8'))
                cursor.execute(sql, data)
        except DatabaseError as e:
            print(f"Coś poszło nie tak: {e}")

    def load_user_by_username(self, username: str):
        
        try:
            with save_data_to_db() as cursor:
                sql = "SELECT username, first_name, last_name FROM users WHERE username = %s;"
                data = (username,)
                cursor.execute(sql, data)
                result = cursor.fetchone()
                
                return result[0] 
        
        except DatabaseError as e:
            print(f"Uzytkownik o takiej nazwie nie istnieje {e}")


    def load_user_by_id(self, id: int):
        
        try:
            with save_data_to_db() as cursor:
                sql = "SELECT username, first_name, last_name FROM users WHERE id = %s;"
                data = (id,)
                cursor.execute(sql, data)
                result = cursor.fetchone()
                
                return result[0] 
        
        except DatabaseError as e:
            print(f"Uzytkownik o takim id nie istnieje {e}")

    @staticmethod
    def load_all_users():

        try:
            with save_data_to_db() as cursor:
                sql = "SELECT username, first_name, last_name FROM users;"
                cursor.execute(sql)
                result = cursor.fetchall()
                
                return result
        
        except DatabaseError as e:
            print(e)       

    def _delete(self, username):

        try:
            with save_data_to_db() as cursor:
                sql = "DELETE FROM users WHERE username = %s;"
                cursor.execute(sql, (username,))
                print(f"Usunięto uzytkonika o nazwie {username}")
        
        except DatabaseError as e:
            print(e)


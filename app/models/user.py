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
        raise
    finally:
        if cursor: cursor.close()
        if ctx: ctx.close()

class User:
    def __init__(self, username, first_name="", last_name="", password=None):
        self._id = -1
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self._hashed_password = None

        if password:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            self._hashed_password = hashed.decode('utf-8')
    
    @property
    def id(self):
        return self._id
    
    @property
    def hashed_password(self):
        return self._hashed_password
    
    def set_new_pass(self, old_password: str, new_password: str) -> str:
        b_old_password = old_password.encode('utf-8')
        
        current_hash = self._hashed_password
        if isinstance(current_hash, str):
            current_hash = current_hash.encode('utf-8')
        
        if bcrypt.checkpw(b_old_password, current_hash):
            new_h = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            self._hashed_password = new_h.decode('utf-8')
            return self._hashed_password
        else:
            print("Hasło nie pasuje")

    
    def _insert(self):
        
        try: 
            with save_data_to_db() as cursor:
                sql = "INSERT INTO users (username, hashed_password, first_name, last_name) VALUES (%s, %s, %s, %s) RETURNING id;"
                data = (self.username, self._hashed_password, self.first_name, self.last_name)
                cursor.execute(sql, data)
        except errors.UniqueViolation:
            print("Uzytkownik o takiej nazwie juz istnieje")
    
    def _update(self):
        try:
            with save_data_to_db() as cursor:
                sql = "UPDATE users SET username=%s, first_name=%s, last_name=%s, hashed_password=%s WHERE username = %s;"
                data = (self.username, self.first_name, self.last_name, self._hashed_password, self.username)
                cursor.execute(sql, data)
        except DatabaseError as e:
            print(f"Coś poszło nie tak: {e}")

    @classmethod
    def load_user_by_username(cls, username: str):
        
        try:
            with save_data_to_db() as cursor:
                sql = "SELECT id, username, first_name, last_name, hashed_password FROM users WHERE username = %s;"
                data = (username,)
                cursor.execute(sql, data)
                result = cursor.fetchone()
                
                if result:
                    user = cls(username=result[1], first_name=result[2], last_name=result[3])
                    user._hashed_password = result[4]
                    user._id = result[0]
                    return user
                
                else:
                    return None     
        
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
                
                users_list = []
                for row in result:
                    users_list.append({"username": row[1],
                                        "first_name": row[2],
                                        "last_name": row[3]
                                       })

                return users_list

        except DatabaseError as e:
            print(e)       
            return []
    
    def _delete(self, username):

        try:
            with save_data_to_db() as cursor:
                sql = "DELETE FROM users WHERE username = %s;"
                cursor.execute(sql, (username,))
                print(f"Usunięto uzytkonika o nazwie {username}")
        
        except DatabaseError as e:
            print(e)

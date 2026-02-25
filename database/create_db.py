from psycopg2 import connect, OperationalError
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("USER")
HOST = os.getenv('HOST')
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

ctx = connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
ctx.autocommit = True

try:
    ctx
except OperationalError:
    print("połączenie nieudane")

create_table_users = """ 
    CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(80) NOT NULL 
    )
"""

create_table_messages = """
    CREATE TABLE IF NOT EXISTS message (
    id SERIAL PRIMARY KEY,
    from_id INT NOT NULL,
    to_id INT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    text VARCHAR(255),
    FOREIGN KEY (from_id) REFERENCES users(id),
    FOREIGN KEY (to_id) REFERENCES users(id)
    )
"""

def exec_sql(sql):
    
    cursor = ctx.cursor()
    cursor.execute(sql)
    cursor.close()

    

exec_sql(create_table_users)
exec_sql(create_table_messages)

ctx.close()

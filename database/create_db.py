from psycopg2 import connect, errors 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("USER")
HOST = os.getenv('HOST')
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

def create_db():
    ctx = connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    ctx.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = ctx.cursor()

    try:
        cursor.execute("CREATE DATABASE message_app_db;")
        print("Baza utworzona")
    except errors.DuplicateDatabase:
        print("Baza juz istnieje")
    finally:
        ctx.close()
        cursor.close()

def create_tables():
    ctx = connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    ctx.autocommit = True
    cursor = ctx.cursor()
    
    queries = {
    
    "users": """  
        CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        hashed_password VARCHAR(80) NOT NULL, 
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL
        )
    """,

    "message": """
        CREATE TABLE IF NOT EXISTS message (
        id SERIAL PRIMARY KEY,
        from_id INT,
        to_id INT,
        creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        text VARCHAR(255),
        FOREIGN KEY (from_id) REFERENCES users(id) ON DELETE SET NULL,
        FOREIGN KEY (to_id) REFERENCES users(id) ON DELETE SET NULL
        )   
    """
    }

    for table_name, sql in queries.items():
        try:
            cursor.execute(sql)
            print("Tabela utworzona")
        except errors.DuplicateTable:
            print(f"Tabela {table_name} już istnieje")

    ctx.close()
    cursor.close()

if __name__ == "__main__":
    create_db()
    create_tables()

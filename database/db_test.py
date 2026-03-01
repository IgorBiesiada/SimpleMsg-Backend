import pytest
from psycopg2 import connect, extensions
from psycopg2.extensions import cursor
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("USER")
HOST = os.getenv('HOST')
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

@pytest.fixture
def connect_db():
    ctx = connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    cursor = ctx.cursor()
    yield cursor

    ctx.rollback()
    cursor.close()
    ctx.close()
    

def test_db_status(connect_db: cursor):
    assert connect_db.connection.status == extensions.STATUS_READY
    

def test_insert_user_into_db(connect_db: cursor):
    
    sql = "INSERT INTO users (username, hashed_password, first_name, last_name) VALUES (%s, %s, %s, %s) RETURNING id;"
    connect_db.execute(sql, ('some_name', 'some_pass', 'some_name', 'some_last_name'))
        
    user_id = connect_db.fetchone()[0]
    assert user_id is not None
    
    connect_db.execute("SELECT username FROM users WHERE id = %s;", (user_id,))
    user = connect_db.fetchone()[0]
    assert user == "some_name"


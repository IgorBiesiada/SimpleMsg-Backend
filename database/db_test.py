import pytest
from psycopg2 import connect, extensions
import os
from dotenv import load_dotenv

load_dotenv()

USER = os.getenv("USER")
HOST = os.getenv('HOST')
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")


def test_db_status():
    ctx = connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    assert ctx.status == extensions.STATUS_READY
    ctx.close()

def test_insert_into_database():
    ctx = connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
    ctx.autocommit = True
    sql = "INSERT "
from psycopg2 import connect, OperationalError

ctx = connect()

create_table_users = """ 
    CREATE TABLE IF NOT EXIST users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(80) NOT NULL 
    )
"""


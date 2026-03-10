from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
import os
from psycopg2 import connect
from psycopg2.extensions import connection as PostgreConnection
from api_models import Token

load_dotenv()

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECREAT_KEY = os.getenv('SECREAT_KEY')
ALGORITHM = os.getenv('ALGORITHM')
USER = os.getenv("USER")
HOST = os.getenv('HOST')
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")



bcrypt_context = CryptContext(schemes=['bcrypt'], deprecadet='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_db():
    try:
        ctx = connect(user=USER, password=PASSWORD, host=HOST, database=DATABASE)
        ctx.autocommit = True
        yield ctx
    
    except Exception as e:
        print(f"Błąd {e}")
        raise
    finally:
        if ctx: ctx.close()

db_dependency = Annotated[PostgreConnection, Depends(get_db)]

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()])
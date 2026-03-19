import httpx
import functools
import os


TOKEN_FILE = ".token"


def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not os.path.exists(TOKEN_FILE):
            print("Musisz sięzalogować")
            return
        
        with open(TOKEN_FILE, "r") as f:
             token = f.read().strip()
        
        func(token, *args, **kwargs)
    return wrapper


def login(username: str, password: str):
    
    response = httpx.post("http://127.0.0.1:8000/auth/token",  data={"username": username, "password": password})

    if response.status_code == 200:
        token = response.json().get("access_token")
        
        if not token:
            print("serwer nie zwrocił tokenu sprawdz dane logowania")
            return
        
        with open(TOKEN_FILE, "w") as f:
            f.write(token)
        print("zalogowano")
    else:
        print("błędne dane")

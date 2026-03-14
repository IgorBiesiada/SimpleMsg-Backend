import httpx

URL = "http://127.0.0.1:8000/auth/token"

payload = {
    "username": "testuser1", 
    "password": "testuser123"
}

def test_connection():
    response = httpx.post(URL, data=payload)

    if response.status_code == 200:
        print("sukces")
    else:
        print("błąd")

test_connection()        